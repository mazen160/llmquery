import requests
import os

"""
Mistral API endpoint example:
curl --location "https://api.mistral.ai/v1/chat/completions" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $MISTRAL_API_KEY" \
     --data '{
    "model": "mistral-large-latest",
    "messages": [{"role": "user", "content": "Who is the most renowned French painter?"}]
  }'
"""

MISTRAL_API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
ACCEPTED_MODELS = ['ministral-3b-latest', 'mistral-small', 'mistral-large-latest', 'mistral-medium', 'open-mistral-nemo', 'mistral-small-latest', 'codestral-latest', 'ministral-8b-latest', 'open-codestral-mamba']
DEFAULT_MODEL = "mistral-small-latest"
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."


def mistral_generate_content(url_endpoint: str = None,
                            mistral_api_key: str = None,
                            model: str = None,
                            system_prompt: str = None,
                            user_prompt: str = None):
    ACCEPTED_MODELS = ["mistral-large-latest", "mistral-medium", "mistral-small", "codestral-latest", "mistral-small-latest", "open-mistral-nemo", "open-codestral-mamba", "ministral-8b-latest", "ministral-3b-latest", "mistral-large-latest", "ministral-3b-latest"]

    if not url_endpoint:
        url_endpoint = MISTRAL_API_ENDPOINT
    if not model:
        model = DEFAULT_MODEL
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    if not mistral_api_key:
        mistral_api_key = os.environ.get("MISTRAL_API_KEY", None)
    if not mistral_api_key:
        raise ValueError("Mistral API key is required.")
    if not user_prompt:
        raise ValueError("User prompt is required.")

    if model not in ACCEPTED_MODELS:
        raise ValueError(f"Model {model} is not supported. Supported models are: {ACCEPTED_MODELS}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mistral_api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    }

    response = requests.post(url_endpoint, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to connect to Mistral API. Status code: {response.status_code}. Response: {response.text}")

    output = {
        "raw_response": response,
        "status_code": response.status_code,
        "data": data,
        "response": ""
    }

    response_json = response.json()
    if not response_json.get("choices"):
        raise Exception(f"Invalid response from Mistral API. Response: {response_json}")

    for choice in response_json.get("choices", []):
        output["response"] += choice.get("message", {}).get("content", "")

    return output


