"""
OpenTelemetry Configuration for xGitGuard
Provides centralized telemetry setup for traces, metrics, and logs
"""

import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def setup_telemetry():
    """
    Initialize OpenTelemetry with OTLP exporters for centralized collection
    """
    
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    service_name = os.getenv("OTEL_SERVICE_NAME", "xgitguard")
    
    trace_provider = TracerProvider(
        resource=Resource.create({"service.name": service_name})
    )
    
    otlp_trace_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
    trace.set_tracer_provider(trace_provider)
    
    otlp_metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    metric_reader = PeriodicExportingMetricReader(
        exporter=otlp_metric_exporter,
        export_interval_millis=30000  # Export every 30 seconds
    )
    
    metric_provider = MeterProvider(
        resource=Resource.create({"service.name": service_name}),
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(metric_provider)
    
    RequestsInstrumentor().instrument()
    
    LoggingInstrumentor().instrument(set_logging_format=True)
    
    return trace.get_tracer(__name__), metrics.get_meter(__name__)


def get_tracer():
    """Get the configured tracer instance"""
    return trace.get_tracer(__name__)


def get_meter():
    """Get the configured meter instance"""
    return metrics.get_meter(__name__)
