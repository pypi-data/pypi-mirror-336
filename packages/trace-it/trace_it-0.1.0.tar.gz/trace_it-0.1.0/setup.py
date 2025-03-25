from setuptools import setup, find_packages

setup(
    name="trace_it",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opentelemetry-api",
        "opentelemetry-sdk",
        "openinference-semantic-conventions",
        "arize-phoenix",
    ],
    python_requires=">=3.8",
)