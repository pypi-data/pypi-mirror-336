from fastapi import Request
from fastapi.responses import StreamingResponse
from trace_it.config.phoenix_tracer import AIObservability
from trace_it.config import context_config 

async def traceit_middleware(request: Request, call_next, project_name: str = "default"):
    # Create an instance of AIObservability
    ai_observer = AIObservability(
        project_name=project_name,
        auto_instrument=False,
    )
    # Get the tracer instance
    tracer = ai_observer.get_tracer(__name__)
    tracer_token = context_config.TRACER_CONTEXT.set(tracer)
    tracer = context_config.TRACER_CONTEXT.get()
    with tracer.start_as_current_span("ParentTrace") as parent_span:
        # Read the request body as bytes
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8')
        parent_span.set_attribute("input.value", body_str)
        trace_token = context_config.TRACE_CONTEXT.set(parent_span)        
        try:
            # Create a new Request with the same body for processing
            # This is needed because we already consumed the body
            request = Request(
                scope=request.scope,
                receive=request._receive
            )
            
            # Process the request
            response = await call_next(request)
            
            # Read response body
            response_body = [chunk async for chunk in response.body_iterator]
            
            # Set the output attribute on the span
            if response_body:
                response_text = b"".join(response_body).decode("utf-8")
                parent_span.set_attribute("output.value", response_text)
            
            # Create a new response with the same body
            return StreamingResponse(
                content=iter(response_body),
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        finally:
            context_config.TRACE_CONTEXT.reset(trace_token)
            context_config.TRACER_CONTEXT.reset(tracer_token)


