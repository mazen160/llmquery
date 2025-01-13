import requests
import os

"""
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
"""


ACCEPTED_MODELS = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-20241022",
    "claude-3-5-haiku-latest",
    "claude-3-opus-20240229",
    "claude-3-opus-latest",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]
DEFAULT_MODEL = "claude-3-5-haiku-latest"
DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


def anthropic_cluade_message(url_endpoint: str = None,
                             anthropic_api_key: str = None,
                             model: str = None,
                             system_prompt: str = None,
                             user_prompt: str = None):
    max_tokens = 8192
    temperature = 0

    if not url_endpoint:
        url_endpoint = DEFAULT_ENDPOINT

    if not model:
        model = DEFAULT_MODEL

    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    if DEFAULT_MODEL not in ACCEPTED_MODELS:
        raise ValueError(f"Model {model} not in accepted models: {ACCEPTED_MODELS}")

    if not user_prompt:
        raise ValueError("User prompt is required.")
    if not anthropic_api_key:
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None)

    if not anthropic_api_key:
        raise ValueError("Anthropic API key is required.")
    headers = {
        "x-api-key": anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url_endpoint, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to connect to Anthropic API. Status code: {response.status_code}. Response: {response}")

    output = {"raw_response": response,
              "status_code": response.status_code,
              "data": data,
              "response": ""}

    if "content" not in response.json():
        raise Exception(f"Invalid response from Anthropic API. Response: {response.json()}")

    for content in response.json()["content"]:
        output["response"] += content.get("text", "")

    return output
