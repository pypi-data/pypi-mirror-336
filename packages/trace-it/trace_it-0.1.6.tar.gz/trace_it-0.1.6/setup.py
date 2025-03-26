from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_discription = f.read()
    
REPO_NAME = "Trace_IT"
AUTHOR_USER_NAME = "Krish-Goyani"
PKG_NAME = "trace_it"
AUTHOR_EMAIL = "krish.goyani@dhiwise.com"

setup(
    name="trace_it",
    version="0.1.6",
    packages=find_packages(exclude=["tests"]),
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for observing traces of your LLM application.",
    long_description=long_discription,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    install_requires=[
        "opentelemetry-api",
        "opentelemetry-sdk",
        "openinference-semantic-conventions",
        "arize-phoenix",
        "fastapi"
    ],
    python_requires=">=3.8",
)
