from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.context import attach, detach, get_current

class TracingLib:
    def __init__(self, service_name: str, http_endpoint: str):
        # Initialize the tracing provider
        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

        # Configure OTLP exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=http_endpoint,
            headers=(("Content-Type", "application/json"),)
        )
        http_span_processor = SimpleSpanProcessor(otlp_exporter)
        provider.add_span_processor(http_span_processor)

        # Console exporter for debugging
        console_exporter = ConsoleSpanExporter()
        console_span_processor = SimpleSpanProcessor(console_exporter)
        provider.add_span_processor(console_span_processor)

        self.tracer = trace.get_tracer(service_name)

    def get_tracer(self):
        # Returns the tracer object
        return self.tracer

    def start_span(self, name: str, attributes: dict = None):
        # Automatically inherit the parent span context if exists
        current_span = trace.get_current_span()
        ctx = get_current()

        # Start a span, linking to parent span if available
        span = self.tracer.start_span(name, context=ctx)
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)

        # Attach the new span to the context
        ctx = trace.set_span_in_context(span)
        token = attach(ctx)

        return span, token

    def end_span(self, span, token):
        # End the span and detach the current context
        span.end()
        detach(token)

    def add_event(self, span, event_name: str, attributes: dict = None):
        # Add an event to a span
        if attributes:
            span.add_event(event_name, attributes=attributes)
        else:
            span.add_event(event_name)
