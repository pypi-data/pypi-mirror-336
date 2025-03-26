from contextvars import ContextVar

# Create a context variable to store the request
TRACE_CONTEXT = ContextVar("trace_context", default=None)
TRACER_CONTEXT = ContextVar("tracer_context", default=None)


