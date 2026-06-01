import os
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from openinference.instrumentation.google_adk import GoogleADKInstrumentor

load_dotenv()

def setup_tracing():
    """Connect to Phoenix Cloud so all ADK agent calls are traced."""
    endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT").rstrip("/")
    api_key = os.getenv("PHOENIX_API_KEY")

    exporter = OTLPSpanExporter(
        endpoint=f"{endpoint}/v1/traces",
        headers={"authorization": f"Bearer {api_key}"},
    )

    resource = Resource(attributes={"openinference.project.name": "worldcup-trip-agent"})
    tp = TracerProvider(resource=resource)
    tp.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(tp)

    GoogleADKInstrumentor().instrument(tracer_provider=tp)
    print("Phoenix tracing connected.")
