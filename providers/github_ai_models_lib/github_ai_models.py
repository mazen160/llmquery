import requests
import os

"""
GitHub AI Models API endpoint example:
curl -X POST "https://models.inference.ai.azure.com/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": "Can you explain the basics of machine learning?"
            }
        ],
        "model": "gpt-4o-mini",
        "temperature": 1,
        "max_tokens": 4096,
        "top_p": 1
    }'
"""

GITHUB_AI_API_ENDPOINT = "https://models.inference.ai.azure.com/chat/completions"
ACCEPTED_MODELS = [
    "DeepSeek-R1",
    "o3-mini",
    "Codestral-2501",
    "Phi-4",
    "Mistral-Large-2411",
    "Llama-3-3-70B-Instruct",
    "Ministral-3B",
    "o1-preview",
    "o1-mini",
    "Meta-Llama-3-1-8B-Instruct",
    "Meta-Llama-3-1-70B-Instruct",
    "Meta-Llama-3-1-405B-Instruct",
    "Mistral-large-2407",
    "Mistral-Nemo",
    "gpt-4o-mini",
    "Mistral-large",
    "Mistral-small",
    "Meta-Llama-3-70B-Instruct",
    "Meta-Llama-3-8B-Instruct",
    "gpt-4o",
]
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."


def github_ai_generate_content(
    url_endpoint: str = None,
    github_token: str = None,
    model: str = None,
    system_prompt: str = None,
    user_prompt: str = None,
):

    temperature = 1
    top_p = 1
    max_tokens = 8192

    if not url_endpoint:
        url_endpoint = GITHUB_AI_API_ENDPOINT
    if not model:
        model = DEFAULT_MODEL
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    if not github_token:
        github_token = os.environ.get("GITHUB_TOKEN", None)
    if not github_token:
        raise ValueError("GitHub API token is required.")
    if not user_prompt:
        raise ValueError("User prompt is required.")

    if model not in ACCEPTED_MODELS:
        raise ValueError(
            f"Model {model} is not supported. Supported models are: {ACCEPTED_MODELS}"
        )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }

    response = requests.post(url_endpoint, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(
            f"Failed to connect to GitHub AI Models API. Status code: {response.status_code}. Response: {response.text}"
        )

    output = {
        "raw_response": response,
        "status_code": response.status_code,
        "data": data,
        "response": "",
    }

    response_json = response.json()
    if not response_json.get("choices"):
        raise Exception(
            f"Invalid response from GitHub AI Models API. Response: {response_json}"
        )

    for choice in response_json.get("choices", []):
        output["response"] += choice.get("message", {}).get("content", "")

    return output
