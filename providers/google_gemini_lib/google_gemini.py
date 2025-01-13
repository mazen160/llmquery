import requests
import os

"""
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }]
   }'
"""

GOOGLE_GEMINI_GENERATECONTENT_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
ACCEPTED_MODELS = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
DEFAULT_MODEL = "gemini-1.5-flash"
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


def google_gemini_generate_content(url_endpoint: str = None,
                                   google_gemini_api_key: str = None,
                                   model: str = None,
                                   system_prompt: str = None,
                                   user_prompt: str = None):

    if not url_endpoint:
        url_endpoint = GOOGLE_GEMINI_GENERATECONTENT_API_ENDPOINT
    if not model:
        model = DEFAULT_MODEL
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    if not google_gemini_api_key:
        google_gemini_api_key = os.environ.get("GOOGLE_GEMINI_API_KEY", None)
    if not google_gemini_api_key:
        raise ValueError("GOOGLE GEMINI API key is required.")
    if not user_prompt:
        raise ValueError("User prompt is required.")

    if model not in ACCEPTED_MODELS:
        raise ValueError(f"Model {model} is not supported. Supported models are: {ACCEPTED_MODELS}")

    headers = {
        "Content-Type": "application/json",
    }

    prepared_prompt = f"{system_prompt}\n\n{user_prompt}"

    data = {
        "contents": [{
            "parts": [{"text": prepared_prompt}]
        }]
    }
    params = {"key": google_gemini_api_key}
    url_endpoint = url_endpoint.format(MODEL=model)
    response = requests.post(url_endpoint, headers=headers, params=params, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to connect to GOOGLE GEMINI API. Status code: {response.status_code}. Response: {response.text}")

    output = {"raw_response": response,
              "status_code": response.status_code,
              "data": data,
              "response": ""}

    if not response.json().get("candidates"):
        raise Exception(f"Invalid response from GOOGLE GEMINI API. Response: {response.json()}")

    for candidate in response.json()["candidates"]:
        for part in candidate["content"]["parts"]:
            output["response"] += part["text"]

    return output
