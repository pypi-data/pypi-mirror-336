# TracingLib: OpenTelemetry Tracing for Python

`TracingLib` is a Python library designed to simplify the integration of OpenTelemetry tracing into your Python applications. Easily create, manage, and link spans for your operations, with support for both automatic parent-child span linking or explicitly defined relationships.

## Installation

Make sure to install the necessary OpenTelemetry Python packages:

```bash
pip install TracingLib
```

# Usage
## Initialize the Tracer

Initialize TracingLib at the start of your application, providing a service name and the OTLP endpoint where traces will be exported. This sets up the TracerProvider and exporter configuration.

```python
from tracing_lib import TracingLib

# Initialize the tracing library
http_endpoint = "http://your-otlp-endpoint/traces"
tracing_lib = TracingLib(service_name="your_service_name", http_endpoint=http_endpoint)
```

# Create and Manage Spans
To trace an operation, start a span and optionally pass a parent span if you're explicitly managing span hierarchies. Add events or attributes to the span to record specific events or metadata during the operation.

```python
# Start a span
span, token = tracing_lib.start_span("operation_name", {"attribute_key": "attribute_value"})

# Add events to the span
tracing_lib.add_event(span, "event_name", {"event_detail": "event_value"})

# End the span when the operation is complete
tracing_lib.end_span(span, token)
```

## Passing a Parent Span
If you want to explicitly pass a parent span (to create a child span), you can do so using the parent_span argument when calling start_span.

```python
# Create a child span with an explicit parent span
child_span, child_token = tracing_lib.start_span("child_operation", parent_span=parent_span)
```

## Learning Notes
1. We are using SimpleSpanProcessor - so to send update each time a span created/updated. Alternatively we can use BatchSpanProcessor that can do batch processing and sending of traces.
2. OpenTelemetry allows setting the TracerProvider only once during the application's lifetime. If you try to set it again, it will throw a warning. So differentiate on basis of span names, attributes or events.
3. We have granular control of spans lifecycle, so remember to start and end the spans to close tracing.
4. The http endpoint should support `application/x-protobuf` type input to receive the traces.
5. The http endpoint would be needing the proto files from https://github.com/open-telemetry/opentelemetry-proto.


# Publishing

## Installation

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http protobuf==4.25.5
```

OR

```bash
pip install -r requirements.txt
```

## Build
```bash
pip install twine setuptools wheel
python setup.py sdist bdist_wheel
```

## Upload
```bash
twine upload dist/*
```
