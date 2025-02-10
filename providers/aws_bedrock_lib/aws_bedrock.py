import boto3
import json
import os
from typing import Dict, Any

# Configuration constants
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ALLOWED_MODELS = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
]
DEFAULT_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
MAX_TOKENS = 8129
ANTHROPIC_VERSION = "bedrock-2023-05-31"
DEFAULT_TEMPERATURE = 1.0
DEFAULT_TOP_K = 250
DEFAULT_TOP_P = 0.999
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


def aws_bedrock_generate_content(
    model: str = None,
    system_prompt: str = None,
    user_prompt: str = None,
    aws_region: str = None,
    max_tokens: int = MAX_TOKENS,
    anthropic_version: str = None,
) -> Dict[str, Any]:
    """
    Generate content using AWS Bedrock's models.

    Args:
        aws_region: AWS region for the Bedrock service
        model: The model ID to use for generation
        system_prompt: Optional system prompt to prepend
        user_prompt: The user's input prompt

    Returns:
        Dictionary containing the response and metadata
    """
    if not user_prompt:
        raise ValueError("User prompt is required.")

    if not model:
        model = DEFAULT_MODEL
    if model not in ALLOWED_MODELS:
        raise ValueError(
            f"Model {model} is not supported. Supported models are: {ALLOWED_MODELS}"
        )
    if not anthropic_version:
        anthropic_version = ANTHROPIC_VERSION

    if not user_prompt:
        raise ValueError("User prompt is required.")

    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    region = aws_region or AWS_REGION

    # Initialize AWS Bedrock runtime client
    bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name=region)

    payload = {
        "anthropic_version": anthropic_version,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "temperature": DEFAULT_TEMPERATURE,
        "top_k": DEFAULT_TOP_K,
        "top_p": DEFAULT_TOP_P,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    }
                ],
            }
        ],
    }
    print(payload)

    response = bedrock_runtime.invoke_model(
        modelId=model,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(response["body"].read())

    result = ""
    for content in response_body.get("content", []):
        result += content.get("text", "")

    output = {
        "raw_response": response_body,
        "status_code": response.get("ResponseMetadata", {}).get("HTTPStatusCode", 200),
        "data": payload,
        "response": result,
    }

    return output
