from setuptools import setup, find_packages

setup(
    name="TracingLib",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        'opentelemetry-api',
        'opentelemetry-sdk',
        "opentelemetry-exporter-otlp-proto-http",
        "protobuf>=3.19,<5.0",
    ],
    description="A package to manage OpenTelemetry tracing, spans, and events.",
    author="Rahul Singh Chauhan",
    author_email="chauhan.rahul2605@gmail.com",
)

