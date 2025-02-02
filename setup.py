# setup.py
from setuptools import setup, find_packages
import os


def list_files(directory):
    paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths


templates_files = list_files("llmquery-templates")


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="llmquery",
    version="0.1.15",
    author="Mazin Ahmed",
    author_email="mazin@mazinahmed.net",
    description="A package for querying various LLM providers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mazen160/llmquery",
    packages=find_packages(
        include=[
            "llmquery*",
            "providers*",
            "query_parser*",
            "providers.anthropic_lib*",
            "providers.google_gemini_lib*",
            "providers.openai_lib*",
            "providers.ollama_lib*",
            "providers.aws_bedrock_lib*",
            "providers.deepseek_lib*",
            "providers.github_ai_models_lib*",
            "providers.mistral_lib*",
        ]
    ),
    data_files=[("llmquery-templates", templates_files)],
    entry_points={"console_scripts": ["llmquery=llmquery.__main__:main"]},
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
