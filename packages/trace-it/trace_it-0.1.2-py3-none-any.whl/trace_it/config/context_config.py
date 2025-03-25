from contextvars import ContextVar

# Create a context variable to store the request
TRACE_CONTEXT = ContextVar("trace_context", default=None)
TRACER_CONTEXT = ContextVar("tracer_context", default=None)




def get_trace_context():
    return TRACE_CONTEXT.get()

def set_trace_context(trace_context):
    TRACE_CONTEXT.set(trace_context)

def get_tracer_context():
    return TRACER_CONTEXT.get()

def set_tracer_context(tracer_context):
    TRACER_CONTEXT.set(tracer_context)


def reset_trace_context(token):
    TRACE_CONTEXT.reset(token)
    
def reset_tracer_context(token):
    TRACER_CONTEXT.reset(token)


