import os
from phoenix.otel import register
from opentelemetry.trace import Tracer
from trace_it.config.context_config import set_tracer_context

class AIObservability:
    def __init__(
        self,
        api_key: str,
        project_name: str = "default",
        collector_endpoint: str = "https://app.phoenix.arize.com",
        auto_instrument: bool = False,
    ):
        """
        Initialize AIObservability instance and set up the Phoenix tracer.

        Args:
            api_key (str): API key for Phoenix Arize.
            project_name (str, optional): Project name for tracing. Defaults to "default".
            collector_endpoint (str, optional): Phoenix collector endpoint. Defaults to official endpoint.
            auto_instrument (bool, optional): Enable/disable auto instrumentation. Defaults to False.
        """
        self.api_key = api_key
        self.project_name = project_name
        self.collector_endpoint = collector_endpoint
        self.auto_instrument = auto_instrument

        # Set environment variables
        self._configure_environment()

        # Register the tracer
        self.tracer_provider = register(
            project_name=self.project_name,
            auto_instrument=self.auto_instrument,
        )

    def _configure_environment(self):
        """Configure environment variables for Phoenix tracing."""
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={self.api_key}"
        os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={self.api_key}"
        os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = self.collector_endpoint

    def get_tracer(self, module_name: str = __name__) -> Tracer:
        """
        Get or create a tracer instance and store it in a context variable.

        Args:
            module_name (str, optional): Name of the module to associate with the tracer. Defaults to __name__.

        Returns:
            Tracer: Phoenix tracer instance.
        """
        tracer = self.tracer_provider.get_tracer(module_name)
        set_tracer_context(tracer)
        return tracer
