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

CATALOG_URL = "https://models.github.ai/catalog/models"
GITHUB_AI_API_ENDPOINT = "https://models.github.ai/inference/chat/completions"

STATIC_ACCEPTED_MODELS = [
    # OpenAI
    "openai/gpt-4.1",
    "openai/gpt-4.1-mini",
    "openai/gpt-4o",
    "openai/o1-preview",
    # Meta (Llama)
    "azureml-meta/Meta-Llama-3.1-8B-Instruct",
    "azureml-meta/Meta-Llama-3.1-70B-Instruct",
    "azureml-meta/Meta-Llama-3.1-405B-Instruct",
    # Mistral
    "azureml-mistral/Mistral-Large-2411",
    "azureml-mistral/mistral-medium-2505",
    # Microsoft
    "azureml/Phi-4",
    # Cohere (embeddings)
    "azureml-cohere/Cohere-embed-v3-multilingual",
    "azureml-cohere/Cohere-embed-v3-english",
]

ACCEPTED_MODELS = STATIC_ACCEPTED_MODELS  # For backward compatibility
DEFAULT_MODEL = "openai/gpt-4.1"
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."


def list_catalog_models(token=None):
    """Return list of model IDs from the GitHub Models catalog."""
    token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        return list(STATIC_ACCEPTED_MODELS)
    try:
        r = requests.get(
            CATALOG_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=60,
        )
        r.raise_for_status()
        ids = [
            item.get("id")
            for item in r.json()
            if isinstance(item, dict) and item.get("id")
        ]
        return sorted(set(STATIC_ACCEPTED_MODELS).union(ids))
    except Exception:
        return list(STATIC_ACCEPTED_MODELS)


def get_accepted_models():
    """Get current accepted models (static + dynamic catalog)."""
    return list_catalog_models()


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
