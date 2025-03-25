import time
from langfuse import Langfuse
from typing import Dict, Any, Optional
from observe_traces.config.context_util import langfuse_context
from observe_traces.config.context_util import tracer_context, langfuse_context

class LangfuseClient:
    def __init__(
        self,
        
        langfuse_public_key: str,
        langfuse_secret_key: str,
        langfuse_host: str,
        release: str
    ):
        self.langfuse_public_key = langfuse_public_key
        self.langfuse_secret_key = langfuse_secret_key
        self.langfuse_host = langfuse_host
        self.release = release
        self.langfuse_client = None
        self.token = None
        
    def initialize_langfuse_client(self):
        self.langfuse_client = Langfuse(
            public_key=self.langfuse_public_key,
            secret_key=self.langfuse_secret_key,
            host=self.langfuse_host,
            release=self.release
        )
        self.token = langfuse_context.set(self.langfuse_client)
        
    def close_langfuse_client(self):
        langfuse_context.reset(self.token)
        
class _LangfuseService:
    
    @staticmethod
    async def create_generation_for_LLM(self, trace_id: str, generation_data: Dict[str, Any], name: str) -> Optional[str]:
        
        try:
            time.sleep(10)
            trace = tracer_context.get()
        
            trace.update(
                output = generation_data["output"],
            )
        except Exception as e:
            return None
        
        langfuse_client = langfuse_context.get()
        generation_object = langfuse_client.generation(
            trace_id = trace_id,
            name=name,
        )
        
        generation_object.end(
            model=generation_data["model_name"],
            input=generation_data["input"],
            output=generation_data["output"],
            usage_details={
                "input_token": generation_data["tokens"]["input"],
                "output_token": generation_data["tokens"]["output"],
                "total_token": generation_data["tokens"]["total"]
            },
            cost_details = {
                "input_cost": generation_data["price"]["input"],
                "output_cost": generation_data["price"]["output"],
                "total_cost": generation_data["price"]["total"]
            },
            metadata={
                "provider": generation_data["service_provider"],
                "cost": generation_data["price"]["total"],
                "input_token": generation_data["tokens"]["input"],
                "output_token": generation_data["tokens"]["output"],
                "total_token": generation_data["tokens"]["total"]
            },
        )
        
        time.sleep(10)
        return generation_object.id
    
    @staticmethod
    async def create_span_for_vectorDB(self, trace_id: str, span_data: Dict[str, Any], name: str) -> Optional[str]:
  
        langfuse_client = langfuse_context.get()
        span_object = langfuse_client.span(
            trace_id = trace_id,
            name=name,
        )
        
        span_object.end(
            input = span_data["query"],
            output = span_data["response"][0]["text"],
            start_time = span_data["start_time"],
            end_time = span_data["end_time"],
            metadata = {
                "operation_type": span_data["operation_type"],
                "provider": span_data["service_provider"],
                "cost": span_data["price"],
                "read_units": span_data["units"],
            }
        )
        
        time.sleep(10)
        return span_object.id
        
    @staticmethod
    async def create_span_for_embedding(self, trace_id: str, span_data: Dict[str, Any], name: str) -> Optional[str]:

        try:
            time.sleep(10)
            trace = tracer_context.get()
    
            trace.update(
                input = span_data["input"],
            )
        except Exception as e:
            return None
        
        langfuse_client = langfuse_context.get()
        span_object = langfuse_client.span(
            trace_id = trace_id,
            name=name,
        )
        
        span_object.end(
            input=span_data["input"],
            start_time=span_data["start_time"],
            end_time=span_data["end_time"],
            metadata={
                "provider": span_data["service_provider"],
                "model_name" : span_data["model_name"],
                "input count" : span_data["input_count"],
                "cost": span_data["price"]["total"],
                "token usage" : span_data["tokens"],
                "price" : span_data["price"],
                "embedding_dimensions": span_data["embedding_dimensions"],
                "response_time": span_data["response_time"],
                "timestamp": span_data["timestamp"]
            },
        )
        
        time.sleep(10)
        return span_object.id
    
    @staticmethod
    async def create_span_for_reranking(self, trace_id: str, span_data: Dict[str, Any], name: str) -> Optional[str]:

        langfuse_client = langfuse_context.get()
        span_object = langfuse_client.span(
            trace_id = trace_id,
            name=name,
        )
        
        span_object.end(
            input= {
                "query": span_data["query"],
                "documents": span_data["documents"]
            },
            output=span_data["rerank_results"],
            start_time=span_data["start_time"],
            end_time=span_data["end_time"],
            metadata={
                "provider": span_data["service_provider"],
                "model_name" : span_data["model_name"],
                "output_count" : span_data["document_count"],
                "cost": span_data["price"],
                "token usage" : span_data["tokens"]["rerank_units"],
                "response_time": span_data["response_time"],
                "timestamp": span_data["timestamp"],
                "top_n" : span_data["top_n"]
            },
        )
        
        time.sleep(10)
        
        return span_object.id