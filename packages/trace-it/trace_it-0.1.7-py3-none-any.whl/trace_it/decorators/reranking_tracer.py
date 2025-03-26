import functools
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict

from trace_it.tracer.phoenix_tracing import tracing_service
from trace_it.config.context_config import TRACE_CONTEXT





def calculate_pinecone_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "pinecone-rerank-v0": 0.10,  # Example: $0.10 per 1k rerank units
    }
    rerank_units = tokens_data.get("rerank_units", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = (rerank_units / 1000) * model_price
    return {
        "rerank_units": rerank_units,
        "price_per_1K": model_price,
        "total": total_price,
    }


def calculate_cohere_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "rerank-english-v3.0": 0.15,  # Example: $0.15 per search unit
    }
    search_units = tokens_data.get("search_units", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = search_units * model_price
    return {
        "search_units": search_units,
        "price_per_unit": model_price,
        "total": total_price,
    }


def calculate_jina_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "jina-reranker-v2-base-multilingual": 0.08,  # Example: $0.08 per 1M tokens
    }
    token_count = tokens_data.get("tokens", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = (token_count / 1000000) * model_price
    return {
        "tokens": token_count,
        "price_per_1M": model_price,
        "total": total_price,
    }


def calculate_voyage_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "rerank-2": 0.12,  # Example: $0.12 per 1M tokens
    }
    token_count = tokens_data.get("tokens", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = (token_count / 1000000) * model_price
    return {
        "tokens": token_count,
        "price_per_1M": model_price,
        "total": total_price,
    }


# Token parsers for different reranking providers
def parse_pinecone_rerank_tokens(
    response_data: Dict[str, Any],
) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {"rerank_units": usage.get("rerank_units", 0)}


def parse_cohere_rerank_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from cohere response
    meta = response_data.get("meta", {})
    billed_units = meta.get("billed_units", {})
    return {
        "search_units": billed_units.get("search_units", 0),
    }


def parse_jina_rerank_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from jina response
    usage = response_data.get("usage", {})
    return {
        "tokens": usage.get("total_tokens", 0),
    }


def parse_voyage_rerank_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from voyage response
    usage = response_data.get("usage", {})
    return {
        "tokens": usage.get("total_tokens", 0),
    }


RERANKING_PROVIDER_CONFIGS = {
    "pinecone": {
        "token_parser": parse_pinecone_rerank_tokens,
        "price_calculator": calculate_pinecone_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
    "cohere": {
        "token_parser": parse_cohere_rerank_tokens,
        "price_calculator": calculate_cohere_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
    "jina": {
        "token_parser": parse_jina_rerank_tokens,
        "price_calculator": calculate_jina_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
    "voyage": {
        "token_parser": parse_voyage_rerank_tokens,
        "price_calculator": calculate_voyage_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
}


def register_reranking_provider(
    provider_name: str,
    token_parser: Callable,
    price_calculator: Callable,
    rerank_results_extractor: Callable,
):
    # Register a new reranking provider with configurations
    RERANKING_PROVIDER_CONFIGS[provider_name] = {
        "token_parser": token_parser,
        "price_calculator": price_calculator,
        "rerank_results_extractor": rerank_results_extractor,
    }


def reranking_tracing(provider: str):
    """
    Decorator for tracing reranking API calls with provider-specific handling.

    Args:
        provider: Name of the reranking provider (e.g., "pinecone", "cohere", "jina", "voyage")
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            model_name = kwargs.get(
                "model_name", args[1] if len(args) > 1 else ""
            )
            query = kwargs.get("query", args[2] if len(args) > 2 else "")
            documents = kwargs.get(
                "documents", args[3] if len(args) > 3 else []
            )
            top_n = kwargs.get("top_n", args[4] if len(args) > 4 else 0)

            parent_span = TRACE_CONTEXT.get()
            if parent_span:
                span_context = parent_span.get_span_context()
                trace_id = str(span_context.trace_id)

            provider_config = RERANKING_PROVIDER_CONFIGS.get(provider, {})
            if not provider_config:
                return await func(*args, **kwargs)

            start_time = time.perf_counter()
            ist = timezone(timedelta(hours=5, minutes=30))

            try:
                # Call the reranking function
                result = await func(*args, **kwargs)

                end_time = time.perf_counter()
                response_time = end_time - start_time

                # Extract token data
                tokens_data, rerank_results = extract_rerank_data(
                    provider, provider_config, result, documents
                )

                # Calculate price if token data is available
                price_data = provider_config["price_calculator"](
                    model_name, tokens_data
                )

                trace_data = {
                    "id": trace_id,
                    "service_provider": provider,
                    "model_name": model_name,
                    "tokens": tokens_data,
                    "price": price_data,
                    "query": query,
                    "documents": documents,
                    "document_count": len(documents),
                    "top_n": top_n,
                    "rerank_results": rerank_results,
                    "response_time": response_time,
                    "timestamp": datetime.now(ist).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                tracing_service.add_reranker_span(
                    span_name="Re.Ranker.Operation", data=trace_data
                )
                return result

            except Exception as e:
                error_trace = {
                    "id": trace_id,
                    "service_provider": provider,
                    "model_name": model_name,
                    "error": str(e),
                    "query": query,
                    "documents": documents,
                    "document_count": len(documents),
                    "top_n": top_n,
                    "timestamp": datetime.now(ist).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                tracing_service.add_error_span(
                    span_name="Error.Re.Ranker.Operation",
                    error_data=error_trace,
                )
                raise e

        return wrapper

    return decorator


def extract_rerank_data(provider, provider_config, result, documents):
    """
    Extract token data and rerank results based on provider.
    """
    tokens_data = {}
    rerank_results = []

    if isinstance(result, tuple):
        raw_response = result[1] if len(result) > 1 else None
        rerank_results = result[0] if len(result) > 0 else []
    else:
        raw_response = result

    if raw_response:
        tokens_data = provider_config["token_parser"](raw_response)

    if provider == "pinecone":
        # Handle Pinecone response
        if "data" in raw_response:
            for doc in raw_response["data"]:
                try:
                    rerank_results.append(
                        {
                            "id": doc.get(
                                "id", ""
                            ),  # Use .get() to avoid KeyError
                            "text": documents[doc.get("index", 0)][
                                "text"
                            ],  # Use .get() for index
                            "relevance_score": doc.get(
                                "score", 0.0
                            ),  # Use .get() for score
                        }
                    )
                except (KeyError, IndexError) as e:

                    continue
        else:
            pass

    elif provider == "voyage":
        # rerank_results = [documents[doc["index"]] for doc in result["data"]]
        if "data" in raw_response:
            for doc in raw_response["data"]:
                try:
                    # Get the index of the document in the original documents list
                    doc_index = doc.get("index", -1)
                    if doc_index >= 0 and doc_index < len(documents):
                        # Map the index back to the original documents to get the id and text
                        original_doc = documents[doc_index]
                        rerank_results.append(
                            {
                                "id": original_doc.get(
                                    "id", ""
                                ),  # Use .get() to avoid KeyError
                                "text": original_doc.get(
                                    "text", ""
                                ),  # Use .get() for text
                                "relevance_score": doc.get(
                                    "relevance_score", 0.0
                                ),  # Use .get() for relevance_score
                            }
                        )
                    else:
                        pass
                except KeyError as e:
                    continue
    elif provider in {"cohere", "jina"}:
        rerank_results = provider_config["rerank_results_extractor"](
            raw_response
        )

    return tokens_data, rerank_results
