from contextvars import ContextVar
from fastapi import Request
from langfuse.client import StatefulTraceClient, Langfuse

request_context: ContextVar[Request] = ContextVar("request_context", default=None)
tracer_context: ContextVar[StatefulTraceClient] = ContextVar("tracer_context", default=None)
langfuse_context: ContextVar[Langfuse] = ContextVar("langfuse_context", default=None)