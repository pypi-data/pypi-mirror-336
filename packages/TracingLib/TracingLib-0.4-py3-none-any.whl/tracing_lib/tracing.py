from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter, BatchSpanProcessor, SpanExportResult
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.context import attach, detach, get_current
from opentelemetry.propagate import inject, extract

class TracingLib:
    def __init__(self, service_name: str, http_endpoint: str, provider=None, debug=False, batch=False):
        if provider is None:
            resource = Resource.create({"service.name": service_name})
            provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(provider)

            # Configure OTLP exporter
            # We are using protobuf format to send traces
            headers = {
                "content-type": 'application/x-protobuf'
            }
            otlp_exporter = OTLPSpanExporter(
                endpoint=http_endpoint,
                headers=headers
            )
            if batch:
                # TODO: to be tested.
                http_span_processor = BatchSpanProcessor(otlp_exporter)
            else:
                http_span_processor = SimpleSpanProcessor(otlp_exporter)
            
            provider.add_span_processor(http_span_processor)

            # Console exporter for debugging
            if debug:
                console_exporter = ConsoleSpanExporter()
                console_span_processor = SimpleSpanProcessor(console_exporter)
                provider.add_span_processor(console_span_processor)

        self.tracer = trace.get_tracer(service_name)
        self.provider = provider  # Save the provider instance to avoid reinitialization

    def get_tracer(self):
        return self.tracer

    def start_span(self, name: str, attributes: dict = None, parent_span=None, context=None):
        # If no parent span is passed, use the current context
        if context:
            ctx = context
        else:
            if parent_span is None:
                ctx = get_current()
            else:
                ctx = trace.set_span_in_context(parent_span)

        # Start the span with the given context (parent or current)
        span = self.tracer.start_span(name, context=ctx)
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)

        # Set this span as the current span and return it
        ctx = trace.set_span_in_context(span)
        token = attach(ctx)

        return span, token

    def end_span(self, span, token):
        span.end()
        detach(token)

    def add_event(self, span, event_name: str, attributes: dict = None):
        if attributes:
            span.add_event(event_name, attributes=attributes)
        else:
            span.add_event(event_name)

    def inject_trace_context(self, carrier):
        inject(carrier)

    def extract_trace_context(self, carrier):
        return extract(carrier)
