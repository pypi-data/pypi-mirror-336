import json

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from src.config.context_config import get_trace_context, get_tracer_context



class SpanAttributes:
    INPUT_VALUE = "input.value"
    INPUT_MIME_TYPE = "input.mime_type"
    OUTPUT_VALUE = "output.value"
    OUTPUT_MIME_TYPE = "output.mime_type"
    LLM_PROVIDER = "llm.provider"
    LLM_MODEL_NAME = "llm.model_name"
    LLM_INPUT_MESSAGES = "llm.input_messages"
    LLM_TOKEN_COUNT_TOTAL = "llm.token_count.total"
    LLM_TOKEN_COUNT_PROMPT = "llm.token_count.prompt"
    LLM_TOKEN_COUNT_COMPLETION = "llm.token_count.completion"
    METADATA = "metadata"
    OPENINFERENCE_SPAN_KIND = "openinference.span.kind"
    INPUT_VALUE = "input.value"
    INPUT_MIME_TYPE = "input.mime_type"
    OUTPUT_VALUE = "output.value"  # Not used here as embedding output vectors aren't provided
    OUTPUT_MIME_TYPE = "output.mime_type"
    EMBEDDING_EMBEDDINGS = "embedding.embeddings"
    EMBEDDING_MODEL_NAME = "embedding.model_name"
    EMBEDDING_PROVIDER = "embedding.provider"  # Custom extension
    METADATA = "metadata"
    OPENINFERENCE_SPAN_KIND = "openinference.span.kind"
    RETRIEVAL_DOCUMENTS = "retrieval.documents"
    RETRIEVAL_PROVIDER = "retrieval.provider"  # Custom extension for vector DB
    RETRIEVAL_TOP_K = "retrieval.top_k"
    RERANKER_INPUT_DOCUMENTS = "reranker.input_documents"
    RERANKER_OUTPUT_DOCUMENTS = "reranker.output_documents"
    RERANKER_QUERY = "reranker.query"
    RERANKER_MODEL_NAME = "reranker.model_name"
    RERANKER_TOP_K = "reranker.top_k"
    RERANKER_PROVIDER = "reranker.provider"  # Custom extension
    METADATA = "metadata"
    OPENINFERENCE_SPAN_KIND = "openinference.span.kind"
    EXCEPTION_MESSAGE = "exception.message"
    EXCEPTION_TYPE = "exception.type"


class EmbeddingAttributes:
    EMBEDDING_TEXT = "embedding.text"
    EMBEDDING_VECTOR = "embedding.vector"


class DocumentAttributes:
    DOCUMENT_ID = "document.id"
    DOCUMENT_SCORE = "document.score"
    DOCUMENT_CONTENT = "document.content"
    DOCUMENT_METADATA = "document.metadata"


class MessageAttributes:
    MESSAGE_ROLE = "message.role"
    MESSAGE_CONTENT = "message.content"


class OpenInferenceSpanKindValues:
    LLM = "LLM"
    EMBEDDING = "EMBEDDING"
    RETRIEVER = "RETRIEVER"
    RERANKER = "RERANKER"
    UNKNOWN = "UNKNOWN"


class OpenInferenceMimeTypeValues:
    TEXT = "text/plain"
    JSON = "application/json"


class TracingService:
    def __init__(self, tracer):
        self.tracer = tracer

    def add_llm_span(
        self, span_name: str, data_to_log: dict, **additional_params
    ):
        # Retrieve the context from ContextVar
        ctx = get_trace_context()
        if ctx is None:
            print("No tracing context found.")
            return

        trace_data = data_to_log
        with self.tracer.start_as_current_span(
            span_name, context=trace.set_span_in_context(ctx)
        ) as span:
            # Set span kind
            span.set_attribute(
                SpanAttributes.OPENINFERENCE_SPAN_KIND,
                OpenInferenceSpanKindValues.LLM,
            )
            # Core attributes
            span.set_attribute(
                f"{SpanAttributes.METADATA}.trace_id", str(trace_data["id"])
            )
            span.set_attribute(
                SpanAttributes.LLM_PROVIDER, trace_data["service_provider"]
            )
            span.set_attribute(
                SpanAttributes.LLM_MODEL_NAME, trace_data["model_name"]
            )
            span.set_attribute(
                SpanAttributes.INPUT_VALUE, trace_data["user_query"]
            )
            span.set_attribute(
                SpanAttributes.INPUT_MIME_TYPE, OpenInferenceMimeTypeValues.TEXT
            )
            span.set_attribute(
                SpanAttributes.OUTPUT_VALUE, trace_data["llm_response"]
            )
            span.set_attribute(
                SpanAttributes.OUTPUT_MIME_TYPE,
                OpenInferenceMimeTypeValues.TEXT,
            )

            # Token handling
            if isinstance(trace_data["tokens"], dict):
                span.set_attribute(
                    SpanAttributes.LLM_TOKEN_COUNT_PROMPT,
                    trace_data["tokens"].get("input", 0),
                )
                span.set_attribute(
                    SpanAttributes.LLM_TOKEN_COUNT_COMPLETION,
                    trace_data["tokens"].get("output", 0),
                )
                span.set_attribute(
                    SpanAttributes.LLM_TOKEN_COUNT_TOTAL,
                    trace_data["tokens"].get("total", 0),
                )
            else:
                span.set_attribute(
                    SpanAttributes.LLM_TOKEN_COUNT_TOTAL, trace_data["tokens"]
                )

            # Custom metadata
            span.set_attribute(
                f"{SpanAttributes.METADATA}.price",
                trace_data["price"].get("total", 0),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.response_time",
                trace_data["response_time"],
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.timestamp", trace_data["timestamp"]
            )

            # Input messages (system and user prompts)
            span.set_attribute(
                f"{SpanAttributes.LLM_INPUT_MESSAGES}.0.{MessageAttributes.MESSAGE_ROLE}",
                "system",
            )
            span.set_attribute(
                f"{SpanAttributes.LLM_INPUT_MESSAGES}.0.{MessageAttributes.MESSAGE_CONTENT}",
                trace_data["system_prompt"],
            )
            span.set_attribute(
                f"{SpanAttributes.LLM_INPUT_MESSAGES}.1.{MessageAttributes.MESSAGE_ROLE}",
                "user",
            )
            span.set_attribute(
                f"{SpanAttributes.LLM_INPUT_MESSAGES}.1.{MessageAttributes.MESSAGE_CONTENT}",
                trace_data["user_prompt"],
            )

    def add_embedding_span(
        self, span_name: str, data: dict, **additional_params
    ):
        ctx = get_trace_context()
        if ctx is None:
            print("No tracing context found.")
            return

        with self.tracer.start_as_current_span(
            span_name, context=trace.set_span_in_context(ctx)
        ) as span:
            # Set span kind
            span.set_attribute(
                SpanAttributes.OPENINFERENCE_SPAN_KIND,
                OpenInferenceSpanKindValues.EMBEDDING,
            )

            # Core embedding attributes
            span.set_attribute(
                f"{SpanAttributes.METADATA}.trace_id", data["id"]
            )
            span.set_attribute(
                SpanAttributes.EMBEDDING_PROVIDER, data["service_provider"]
            )
            span.set_attribute(
                SpanAttributes.EMBEDDING_MODEL_NAME, data["model_name"]
            )

            # Input attributes
            span.set_attribute(
                SpanAttributes.INPUT_VALUE, " ".join(data["inputs"])
            )  # Concatenated inputs
            span.set_attribute(
                SpanAttributes.INPUT_MIME_TYPE, OpenInferenceMimeTypeValues.TEXT
            )

            # Embedding inputs as a list
            for i, input_text in enumerate(data["inputs"]):
                span.set_attribute(
                    f"{SpanAttributes.EMBEDDING_EMBEDDINGS}.{i}.{EmbeddingAttributes.EMBEDDING_TEXT}",
                    input_text,
                )
                # Note: embedding.vector is omitted as vector data isn’t provided

            # Token and price metadata
            span.set_attribute(
                f"{SpanAttributes.METADATA}.token_count.total",
                data["tokens"]["tokens"],
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.price.total", data["price"]["total"]
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.price.tokens",
                data["price"]["tokens"],
            )
            # below is used because phoenix does not support the embedding toke count
            span.set_attribute(
                f"{SpanAttributes.LLM_TOKEN_COUNT_COMPLETION}",
                data["price"]["tokens"],
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.price.price_per_1M",
                data["price"]["price_per_1M"],
            )

            # Additional metadata
            span.set_attribute(
                f"{SpanAttributes.METADATA}.input_count", data["input_count"]
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.embedding_dimensions",
                data["embedding_dimensions"],
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.response_time",
                data["response_time"],
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.timestamp", data["timestamp"]
            )

    def add_vectordb_span(self, span_name: str, data: dict):
        ctx = get_trace_context()
        if ctx is None:
            print("No tracing context found.")
            return

        with self.tracer.start_as_current_span(
            span_name, context=trace.set_span_in_context(ctx)
        ) as span:
            # Set span kind
            span.set_attribute(
                SpanAttributes.OPENINFERENCE_SPAN_KIND,
                OpenInferenceSpanKindValues.RETRIEVER,
            )

            # Core retrieval attributes
            span.set_attribute(
                SpanAttributes.RETRIEVAL_PROVIDER,
                data.get("service_provider", ""),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.operation_type",
                data.get("operation_type", ""),
            )

            # Response as retrieval.documents
            response = data.get("response", [])
            for i, doc in enumerate(response):
                span.set_attribute(
                    f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_SCORE}",
                    doc.get("score", 0.0),
                )
                span.set_attribute(
                    f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_CONTENT}",
                    doc.get("text", ""),
                )
                span.set_attribute(
                    f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_METADATA}",
                    json.dumps({"namespace": doc.get("namespace", "")}),
                )

            # Operation details
            operation_details = data.get("operation_details", {})
            span.set_attribute(
                f"{SpanAttributes.METADATA}.index_host",
                operation_details.get("index_host", ""),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.namespace",
                operation_details.get("namespace", ""),
            )
            span.set_attribute(
                SpanAttributes.RETRIEVAL_TOP_K,
                operation_details.get("top_k", 0),
            )

            # Additional metadata
            span.set_attribute(
                f"{SpanAttributes.METADATA}.units", data.get("units", 0)
            )
            # phoenix dont support the tokens for the vectord db operations so added as the llm tokens
            span.set_attribute(
                f"{SpanAttributes.LLM_TOKEN_COUNT_COMPLETION}",
                data.get("units", 0),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.price", data.get("price", 0.0)
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.response_time",
                data.get("response_time", 0.0),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.timestamp",
                data.get("timestamp", ""),
            )

    def add_reranker_span(self, span_name: str, data: dict):
        ctx = get_trace_context()
        if ctx is None:
            print("No tracing context found.")
            return

        with self.tracer.start_as_current_span(
            span_name, context=trace.set_span_in_context(ctx)
        ) as span:
            # Set span kind
            span.set_attribute(
                SpanAttributes.OPENINFERENCE_SPAN_KIND,
                OpenInferenceSpanKindValues.RERANKER,
            )

            # Core reranker attributes
            span.set_attribute(
                f"{SpanAttributes.METADATA}.trace_id", data.get("id", "")
            )
            span.set_attribute(
                SpanAttributes.RERANKER_PROVIDER,
                data.get("service_provider", ""),
            )
            span.set_attribute(
                SpanAttributes.RERANKER_MODEL_NAME, data.get("model_name", "")
            )
            span.set_attribute(
                SpanAttributes.RERANKER_QUERY, data.get("query", "")
            )

            # Input documents
            input_docs = data.get("documents", [])
            for i, doc in enumerate(input_docs):
                span.set_attribute(
                    f"{SpanAttributes.RERANKER_INPUT_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_ID}",
                    doc.get("id", ""),
                )
                span.set_attribute(
                    f"{SpanAttributes.RERANKER_INPUT_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_CONTENT}",
                    doc.get("text", ""),
                )

            # Output (reranked) documents
            output_docs = data.get("rerank_results", [])
            for i, doc in enumerate(output_docs):
                span.set_attribute(
                    f"{SpanAttributes.RERANKER_OUTPUT_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_ID}",
                    doc.get("id", ""),
                )
                span.set_attribute(
                    f"{SpanAttributes.RERANKER_OUTPUT_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_CONTENT}",
                    doc.get("text", ""),
                )
                span.set_attribute(
                    f"{SpanAttributes.RERANKER_OUTPUT_DOCUMENTS}.{i}.{DocumentAttributes.DOCUMENT_SCORE}",
                    doc.get("relevance_score", 0.0),
                )

            # Additional reranker attributes
            span.set_attribute(
                SpanAttributes.RERANKER_TOP_K, data.get("top_n", 0)
            )

            # Metadata
            # again read units not supportd so we use the llm usage token
            span.set_attribute(
                f"{SpanAttributes.METADATA}.rerank_units",
                data.get("tokens", {}).get("rerank_units", 0),
            )
            span.set_attribute(
                f"{SpanAttributes.LLM_TOKEN_COUNT_COMPLETION}",
                data.get("tokens", {}).get("rerank_units", 0),
            )

            span.set_attribute(
                f"{SpanAttributes.METADATA}.price",
                data.get("price", {}).get("total", 0.0),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.document_count",
                data.get("document_count", 0),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.response_time",
                data.get("response_time", 0.0),
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.timestamp",
                data.get("timestamp", ""),
            )

    def add_error_span(
        self, span_name: str, error_data: dict, error_type: str = "unknown"
    ):
        ctx = get_trace_context()
        if ctx is None:
            print("No tracing context found.")
            return

        with self.tracer.start_as_current_span(
            span_name, context=trace.set_span_in_context(ctx)
        ) as span:
            # Set span kind
            # Set span status to ERROR
            span.set_status(Status(StatusCode.ERROR))
            span.set_attribute(
                SpanAttributes.OPENINFERENCE_SPAN_KIND,
                OpenInferenceSpanKindValues.UNKNOWN,
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.error_type", error_type
            )

            # Common error attributes
            span.set_attribute(
                f"{SpanAttributes.METADATA}.trace_id", error_data.get("id", "")
            )
            span.set_attribute(
                SpanAttributes.EXCEPTION_MESSAGE,
                error_data.get("error", "Unknown error"),
            )
            span.set_attribute(
                SpanAttributes.EXCEPTION_TYPE,
                type(error_data.get("error", "")).__name__,
            )
            span.set_attribute(
                f"{SpanAttributes.METADATA}.timestamp",
                error_data.get("timestamp", ""),
            )

            # Dynamically set all other fields as metadata attributes
            for key, value in error_data.items():
                if key in ["id", "error", "timestamp"]:  # Skip common fields
                    continue
                if isinstance(
                    value, (str, int, float, bool)
                ):  # Handle simple types
                    span.set_attribute(
                        f"{SpanAttributes.METADATA}.{key}", value
                    )
                elif isinstance(value, dict):  # Handle nested dictionaries
                    for sub_key, sub_value in value.items():
                        span.set_attribute(
                            f"{SpanAttributes.METADATA}.{key}.{sub_key}",
                            sub_value,
                        )
                elif isinstance(value, list):  # Handle lists (e.g., documents)
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            for sub_key, sub_value in item.items():
                                span.set_attribute(
                                    f"{SpanAttributes.METADATA}.{key}.{i}.{sub_key}",
                                    sub_value,
                                )
                        else:
                            span.set_attribute(
                                f"{SpanAttributes.METADATA}.{key}.{i}", item
                            )

tracer = get_tracer_context()
tracing_service = TracingService(tracer)
