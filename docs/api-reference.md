# API Reference for `LLMQuery`

Welcome to the API reference for the `LLMQuery` class in the `llmquery` framework. This document provides a detailed overview of the class, its attributes, methods, and usage examples. Written to provide clarity and precision, this guide aims to empower developers to fully utilize `LLMQuery` to interact with Language Model APIs effectively.

---

## Class: `LLMQuery`

The `LLMQuery` class is the core interface for interacting with various LLM providers. It allows users to define prompts using YAML templates, validate inputs, and query the providers.

### Constructor: `LLMQuery()`

#### **Parameters**

| Parameter               | Type   | Description                                                                                    | Required | Default           |
| ----------------------- | ------ | ---------------------------------------------------------------------------------------------- | -------- | ----------------- |
| `provider`              | `str`  | The LLM provider to query. Supported values: `OPENAI`, `ANTHROPIC`, `GOOGLE_GEMINI`, `OLLAMA`. | Yes      | None              |
| `templates_path`         | `str`  | Path to a YAML template directory or file defining the system and user prompts.                             | No       | None              |
| `template_inline`       | `str`  | YAML template as a string (if not using `templates_path`).                                      | No       | None              |
| `template_id`           | `str`  | ID of the template to use when multiple templates exist in the file.                           | No       | None              |
| `variables`             | `dict` | Key-value pairs for dynamic variables in the template.                                         | No       | `{}`              |
| `openai_api_key`        | `str`  | API key for OpenAI.                                                                            | No       | `None` (from ENV) |
| `anthropic_api_key`     | `str`  | API key for Anthropic.                                                                         | No       | `None` (from ENV) |
| `google_gemini_api_key` | `str`  | API key for Google Gemini.                                                                     | No       | `None` (from ENV) |
| `model`                 | `str`  | The model to use for the query (e.g., `gpt-4`).                                                | Yes      | None              |
| `max_tokens`            | `int`  | Maximum number of tokens for the response.                                                     | No       | 8192              |
| `max_length`            | `int`  | Maximum character length for the prompt.                                                       | No       | 2048              |
| `aws_bedrock_region`    | `str`  | AWS region for Bedrock service.                                                               | No       | None              |
| `aws_bedrock_anthropic_version` | `str` | Anthropic version for AWS Bedrock Claude models.                                       | No       | "bedrock-2023-05-31" |


#### **Raises**
- `ValueError`: If required parameters are missing or invalid.
- `FileNotFoundError`: If the specified `templates_path` does not exist.

---

### Methods

#### `Query()`
Executes the query using the defined provider and template.

**Returns:**
The `Query()` method returns a standard output in the following format:

```python
output = {
    "raw_response": response,  # requests.Response object
    "status_code": response.status_code,  # HTTP status code
    "data": data,  # Data sent to the LLM
    "response": ""  # The actual LLM output
}
```
- `raw_response`: A `requests.Response` object containing the raw HTTP response.
- `status_code`: The HTTP status code of the response.
- `data`: The data payload sent to the LLM.
- `response`: The processed output from the LLM.

**Raises:**
- `ValueError`: If the query exceeds token or length limits.
- `Exception`: For provider-specific API errors.

---

## Example Usage

### Basic Query with OpenAI

```python
from llmquery import LLMQuery

query = LLMQuery(
    provider="OPENAI",
    templates_path="./templates/chat-template.yaml",
    variables={"user_input": "What is the capital of France?"},
    openai_api_key="your-api-key",
    model="gpt-4",
)
response = query.Query()
print(response)
```

### Inline Template with Variables

```python
from llmquery import LLMQuery

inline_template = """
id: example-inline

system_prompt: >
    You are a helpful assistant.

prompt: >
    User says: {{ user_input }}

variables:
    user_input: "Hello!"
"""

query = LLMQuery(
    provider="OPENAI",
    template_inline=inline_template,
    openai_api_key="your-api-key",
    model="gpt-4",
)
response = query.Query()
print(response)
```

### Overwriting Variables

```python
query.set_variables({"user_input": "What is the population of Earth?"})
response = query.Query()
print(response)
```

---

## Supported Providers

The `LLMQuery` class supports the following providers:

1. **OpenAI**
    - API Key: Required (`openai_api_key` or `OPENAI_API_KEY` in environment).
    - Models: `gpt-4o`, `gpt-3.5-turbo`, etc.

2. **Anthropic (Claude)**
    - API Key: Required (`anthropic_api_key` or `ANTHROPIC_API_KEY` in environment).
    - Models: `claude-3-5-sonnet-latest`, etc.

3. **Google Gemini**
    - API Key: Required (`google_gemini_api_key` or `GOOGLE_GEMINI_API_KEY` in environment).
    - Models: `gemini-1.5-flash`, etc.

4. **AWS Bedrock**
    - Authentication: Uses AWS credentials from environment or config
    - Region: Specified via `aws_bedrock_region`
    - Models:  AWS Bedrock Models
    - Anthropic Version: Configurable via `aws_bedrock_anthropic_version`

5. **Ollama**
    - API Key: Optional, if required by the specific model.
    - Models: Defined per provider.

---

## Error Handling

The `LLMQuery` class includes robust error handling mechanisms:

1. **Input Validation**
    - Ensures templates are correctly formatted and variables are defined.

2. **Provider-Specific Errors**
    - Handles common API errors, such as unauthorized access or model unavailability.

3. **Custom Exceptions**
    - Raises meaningful exceptions with actionable messages.

---

## Best Practices

1. **Use Environment Variables for API Keys**
   - Avoid hardcoding keys. Use environment variables like `OPENAI_API_KEY`.

3. **Optimize Prompts**
   - Ensure prompts are concise and within token limits to reduce costs and improve performance.

4. **Handle Errors Gracefully**
   - Use `try-except` blocks to handle exceptions and log errors effectively.

---


For more examples and contributions, visit the [GitHub repository](https://github.com/mazen160/llmquery).

