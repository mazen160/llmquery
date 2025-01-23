import requests
import os

"""
DeepSeek API endpoint example:
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -d '{
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "stream": false
      }'
"""

DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/chat/completions"
ACCEPTED_MODELS = ["deepseek-chat", "deepseek-reasoner", "deepseek-coder"]
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


def deepseek_generate_content(url_endpoint: str = None,
                            deepseek_api_key: str = None,
                            model: str = None,
                            system_prompt: str = None,
                            user_prompt: str = None):
    
    if not url_endpoint:
        url_endpoint = DEEPSEEK_API_ENDPOINT
    if not model:
        model = DEFAULT_MODEL
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    if not deepseek_api_key:
        deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY", None)
    if not deepseek_api_key:
        raise ValueError("DeepSeek API key is required.")
    if not user_prompt:
        raise ValueError("User prompt is required.")

    if model not in ACCEPTED_MODELS:
        raise ValueError(f"Model {model} is not supported. Supported models are: {ACCEPTED_MODELS}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {deepseek_api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    response = requests.post(url_endpoint, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to connect to DeepSeek API. Status code: {response.status_code}. Response: {response.text}")

    output = {
        "raw_response": response,
        "status_code": response.status_code,
        "data": data,
        "response": ""
    }

    response_json = response.json()
    if not response_json.get("choices"):
        raise Exception(f"Invalid response from DeepSeek API. Response: {response_json}")

    for choice in response_json.get("choices", []):
        output["response"] += choice.get("message", {}).get("content", "")

    return output

