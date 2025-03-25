import functools
import time
from typing import Dict, Any, Callable
from observe_traces.config.context_util import request_context
from datetime import datetime, timezone, timedelta
from observe_traces.config.langfuse_service import _LangfuseService


def calculate_openai_price(model_name: str, input_tokens: int, output_tokens: int) -> Dict[str, float]:

    pricing = {
        "gpt-3.5-turbo": {"input": 0.15, "output": 0.6},
        "gpt-4o": {"input": 2.5, "output": 10.0},    
        "gpt-4o-mini": {"input": 0.15, "output": 0.6},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "o1-2024-12-17": {"input": 15, "output": 60},
        'o3-mini-2025-01-31': {"input": 1.1, "output": 4.40},
        "o1-mini-2024-09-12x": {"input": 1.1,  "output": 4.40},
        # when new openai models come then just add them over here 
    }
    
    model_pricing = pricing.get(model_name, {"input": 0.0, "output": 0.0})  # Default fallback
    
    input_price = (input_tokens / 1000000) * model_pricing["input"]
    output_price = (output_tokens / 1000000) * model_pricing["output"]
    total_price = input_price + output_price
    
    return {
        "input": input_price , #round(input_price, 6),
        "output": output_price, #round(output_price, 6),
        "total": total_price, #round(total_price, 6)
    }


def calculate_anthropic_price(model_name:str, input_tokens:int, output_tokens:int) -> Dict[str, float]:

    pricing = {
        "claude-3-7-sonnet-20250219" : {"input" : 3,"output" : 15},
        "claude-3-5-sonnet-20241022" : {"input" : 3,"output" : 15},
        "claude-3-5-haiku-20241022" : {"input" : 0.80,"output" : 4},
        "claude-3-opus-20240229" : {"input" : 15,"output" : 75},
        "claude-3-haiku-20240307" : {"input" : 0.25,"output" : 1.25},
    }

    model_pricing = pricing.get(model_name, {"input": 0.0, "output": 0.0}) #default fallback 
    input_price = (input_tokens / 1000000) * model_pricing["input"]
    output_price = (output_tokens / 1000000) * model_pricing["output"]
    total_price = input_price + output_price

    return {
        "input": input_price, #round(input_price, 6),
        "output": output_price,#round(output_price, 6),
        "total": total_price, #round(total_price, 6)
    }


def calculate_groq_price(model_name: str, input_tokens: int, output_tokens: int) -> Dict[str, float]:

    pricing = {
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        "gemma2-9b-it": {"input": 0.2, "output": 0.2},
        "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
        "llama3-70b-8192": {"input": 0.59, "output": 0.79},
        "llama-guard-3-8b": {"input": 0.2, "output": 0.2},
        "llama3-8b-8192": {"input": 0.05, "output": 0.08},
        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
    }
    
    model_pricing = pricing.get(model_name, {"input": 0.0, "output": 0.0})  # Default fallback
    
    input_price = (input_tokens / 1000000) * model_pricing["input"]
    output_price = (output_tokens / 1000000) * model_pricing["output"]
    total_price = input_price + output_price
    
    return {
        "input": round(input_price, 6),
        "output": round(output_price, 6),
        "total": round(total_price, 6)
    }


# Token parsers for different providers
def parse_openai_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {
        "input": usage.get("prompt_tokens", 0),
        "output": usage.get("completion_tokens", 0),
        "total": usage.get("total_tokens", 0)
    }


def parse_groq_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {
        "input": usage.get("prompt_tokens", 0),
        "output": usage.get("completion_tokens", 0),
        "total": usage.get("total_tokens", 0)
    }

def parse_anthropic_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    return {
        "input": input_tokens,
        "output": output_tokens,
        "total": input_tokens + output_tokens
    }



PROVIDER_CONFIGS = {
    "openai": {
        "token_parser": parse_openai_tokens,
        "price_calculator": calculate_openai_price,
        "response_extractor": lambda data: data["choices"][0]["message"]["content"] if "choices" in data and data["choices"] else ""
    },
    "groq": {
        "token_parser": parse_groq_tokens,
        "price_calculator": calculate_groq_price,
        "response_extractor": lambda data: data["choices"][0]["message"]["content"] if "choices" in data and data["choices"] else ""
    },
    "anthropic": {
        "token_parser": parse_anthropic_tokens,
        "price_calculator": calculate_anthropic_price,
        "response_extractor": lambda data: data["content"][0]["text"] if "content" in data and data["content"] else ""
    }
    
    # Add other providers here
}


def register_provider(
    provider_name: str, 
    token_parser: Callable, 
    price_calculator: Callable, 
    response_extractor: Callable
):
    #Register a new LLM provider with configurations here
    PROVIDER_CONFIGS[provider_name] = {
        "token_parser": token_parser,
        "price_calculator": price_calculator,
        "response_extractor": response_extractor
    }


def llm_tracing(provider: str):
    """
    Decorator for tracing LLM API calls with provider-specific handling
    
    Args:
        provider: Name of the LLM provider (e.g., "openai", "groq")
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, model_name, system_prompt, user_prompt, user_query, **params):
            # Generate trace ID if not provided
            # if not trace_id:

            id = request_context.get()
            trace_id = id #str(uuid.uuid4())
                
            # Get provider config
            provider_config = PROVIDER_CONFIGS.get(provider, {})
            if not provider_config:
                # logger.warning(f"No config found for provider: {provider}, falling back to default handling")
                return await func(self, model_name, system_prompt, user_prompt, user_query, **params)
            
           
            start_time = time.perf_counter()
            
            try:
            
                result = await func(self, model_name, system_prompt, user_prompt, user_query, **params)
                
                end_time = time.perf_counter()
                response_time = end_time - start_time
                
               
                if isinstance(result, tuple):
                    response_data = result[0] if len(result) > 0 else None
                    raw_response = result[1] if len(result) > 1 else None
                    # jis hisab se response de rha he funciton ye change krna pdega 
                    llm_response = response_data
                    tokens_data = provider_config["token_parser"](raw_response) if raw_response else {}
                else:
                    # case when function returns entire json response from llm
                    raw_response = result
                    llm_response = provider_config["response_extractor"](raw_response)
                    tokens_data = provider_config["token_parser"](raw_response)
                

                price_data = provider_config["price_calculator"](
                    model_name, 
                    tokens_data.get("input", 0), 
                    tokens_data.get("output", 0)
                )
                ist = timezone(timedelta(hours=5, minutes=30))
                
                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY BELOW ###
                try:
                    # logger.info(f"Creating generation for trace: {trace_id}")
                    generation_data = {
                            "model_name": model_name,
                            "service_provider": provider,
                            "input": user_query,
                            "output": llm_response,
                            "tokens": tokens_data,
                            "price": price_data,
                            "system_prompt": system_prompt,
                            "start_time": datetime.fromtimestamp(start_time),
                            "end_time": datetime.fromtimestamp(end_time),
                        }
                    
                    # logger.info(f"Generation data: {generation_data}")
                    
                    generation_id = await _LangfuseService.create_generation_for_LLM(trace_id, generation_data, f"{provider.capitalize()} Generation")
                    # logger.info(f"Generation created with ID: {generation_id}")
                
                except Exception as e:
                    raise f"Error while creating generation for trace: {trace_id}"
                    
                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY ABOVE ###
               
                return result
                
            except Exception as e:
                raise e
                
        return wrapper
    return decorator
