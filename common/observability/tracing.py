"""
Basic OpenTelemetry tracing that exports to stdout and (optionally) OTLP endpoint.
Configure env vars:
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
"""
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

service_name = os.getenv("SERVICE_NAME", "money-transfer-common")

provider = TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# OTLP exporter if endpoint set
if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")))
    )

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
