import requests
import os

"""
https://api.openai.com/v1/chat/completions
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "developer",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
"""

OPENAI_CHAT_COMPLETION_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
ACCEPTED_MODELS = ["gpt-4o",
                   "gpt-4o-turbo",
                   "gpt-4o-2024-11-20",
                   "gpt-4o-2024-08-06",
                   "gpt-4o-mini",
                   "gpt-4o-mini-2024-07-18",
                   "o1-mini",
                   "o1-mini-2024-09-12",
                   "chatgpt-4o-latest",
                   "gpt-4-turbo",
                   "gpt-4-turbo-2024-04-09",
                   "gpt-4",
                   "gpt-4-32k",
                   "gpt-4-0125-preview",
                   "gpt-4-1106-preview",
                   "gpt-4-vision-preview",
                   "gpt-3.5-turbo-0125",
                   "gpt-3.5-turbo-instruct",
                   "gpt-3.5-turbo-1106",
                   "gpt-3.5-turbo-0613",
                   "gpt-3.5-turbo-16k-0613",
                   "gpt-3.5-turbo-0301",
                   "davinci-002",
                   "babbage-002"
                   ]
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


def openai_chat_completion(url_endpoint: str = None,
                           openai_api_key: str = None,
                           model: str = None,
                           system_prompt: str = None,
                           user_prompt: str = None):

    if not url_endpoint:
        url_endpoint = OPENAI_CHAT_COMPLETION_API_ENDPOINT
    if not model:
        model = DEFAULT_MODEL
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    if not openai_api_key:
        openai_api_key = os.environ.get("OPENAI_API_KEY", None)
    if not openai_api_key:
        raise ValueError("OpenAI API key is required.")
    if not user_prompt:
        raise ValueError("User prompt is required.")

    if model not in ACCEPTED_MODELS:
        raise ValueError(f"Model {model} is not supported. Supported models are: {ACCEPTED_MODELS}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    response = requests.post(url_endpoint, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to connect to OpenAI API. Status code: {response.status_code}. Response: {response.text}")

    output = {"raw_response": response,
              "status_code": response.status_code,
              "data": data,
              "response": ""}

    if "choices" not in response.json():
        raise Exception(f"Invalid response from OpenAI API. Response: {response.json()}")

    for choice in response.json()["choices"]:
        if "message" in choice:
            output["response"] += choice["message"]["content"]

    return output
