<p align="center">
    <img src="https://raw.githubusercontent.com/mazen160/public/refs/heads/master/static/images/llmquery-logo-3.png" alt="llmquery logo">
</p>


<h1 align="center">🌐 llmquery: Scaling GenAI automation 🌐</h1>
<h2 align="center">Powerful LLM Query Framework with YAML Prompt Templates</h2>
<h3 align="center"><a href="https://mazinahmed.net/blog/llmquery-project/">Read the release blog post</a></h3>

---

# 🚀 What is llmquery?

`llmquery` is a comprehensive framework for interacting with Language Model APIs, such as OpenAI, Anthropic, Google Gemini, and Ollama. It leverages standard YAML templates for prompt management, validation, and dynamic generation. Designed to streamline complex workflows, it allows developers to integrate, query, and test LLMs with ease.

Whether you’re building a chatbot, generating creative content, or analyzing data, `llmquery` provides the tools to standardize and optimize LLM interactions.

# 🎬 llmquery in Action

This is an example where llmquery runs with `detect-security-vulnerabilities` template to scan application code.

<p align="center">
    <img src="https://raw.githubusercontent.com/mazen160/public/refs/heads/master/static/images/llmquery-example-code-security-1.png" alt="llmquery logo">
</p>

# Why llmquery?

Language models have become integral to modern applications, but efficiently managing and interacting with multiple providers can be challenging. `llmquery` solves this by offering:

- **Provider-Agnostic Queries**: Support for multiple providers, including OpenAI, Anthropic, Google Gemini, and Ollama.
- **Templated Workflows**: Use YAML-based templates to define dynamic prompts and system configurations.
- **Validation and Error Handling**: Ensure templates are validated, token limits are checked, and errors are surfaced with actionable messages.
- **Extensibility**: Easily extend to support new providers or integrate with custom workflows.

---

# 💡 Key Features

- **Multi-Provider Support**: Interact seamlessly with OpenAI, Anthropic, Google Gemini, and Ollama models.
- **YAML-Based Prompt Management**: Define, validate, and render prompts dynamically.
- **Token & Length Validation**: Prevent token limit errors with built-in checks.
- **Error Handling**: Comprehensive handling of common API and template issues.
- **CLI & Programmatic Access**: Use as a Python library or command-line tool.

---

# 📖 Usage

View the full documentation at the [llmquery documentation](https://github.com/mazen160/llmquery/blob/main/docs/).


## Installation

```bash
$ pip install llmquery
```

or manually:
```bash
$ git clone https://github.com/mazen160/llmquery.git
$ cd llmquery
$ python setup.py install
```

## Basic Example

```python
from llmquery import LLMQuery

diff = """diff --git a/example.py b/example.py
+ def insecure_function(password):
+     print(f"Your password is {password}")
+     # TODO: Replace with secure logging
+
+ user_password = "12345"
+ insecure_function(user_password)
"""

query = LLMQuery(
    provider="ANTHROPIC",
    templates_path="templates/",
    template_id="pr-reviews"
    variables={"diff": diff},
    anthropic_api_key="your-api-key",
    model="claude-3-5-sonnet-latest"
)

response = query.Query()
print(response)
```

### Query OpenAI with a Template

```python
from llmquery import LLMQuery

variables = {"user_input": "Hello, how are you?"}

query = LLMQuery(
    provider="OPENAI",
    template_inline="""
    system_prompt: "You are a helpful assistant."
    prompt: "User says: {{ user_input }}"
    """,
    variables=variables,
    openai_api_key="your-api-key",
    model="gpt-4o-mini",
)

response = query.Query()
print(response)
```



## CLI Usage

```bash
$ llmquery -h
Welcome to llmquery CLI!
Scaling GenAI automation 🚀🌐


██      ██      ███    ███  ██████  ██    ██ ███████ ██████  ██    ██
██      ██      ████  ████ ██    ██ ██    ██ ██      ██   ██  ██  ██
██      ██      ██ ████ ██ ██    ██ ██    ██ █████   ██████    ████
██      ██      ██  ██  ██ ██ ▄▄ ██ ██    ██ ██      ██   ██    ██
███████ ███████ ██      ██  ██████   ██████  ███████ ██   ██    ██
                               ▀▀


usage: llmquery [-h] [--provider {OPENAI,ANTHROPIC,GOOGLE_GEMINI,OLLAMA}] [--templates-path TEMPLATES_PATH] [--template-id TEMPLATE_ID] [--variables VARIABLES]
                [--variables-file VARIABLES_FILE] [--model MODEL] [--max-tokens MAX_TOKENS] [--max-length MAX_LENGTH] [--api-key API_KEY]

[bold cyan]A CLI for querying LLMs using YAML templates with llmquery.[/bold cyan]

options:
  -h, --help            show this help message and exit
  --provider {OPENAI,ANTHROPIC,GOOGLE_GEMINI,OLLAMA}
                        Specify the LLM provider to use (e.g. OPENAI, ANTHROPIC, GOOGLE_GEMINI, OLLAMA).
  --templates-path TEMPLATES_PATH
                        Path to the YAML templates directory defining the query.
  --template-id TEMPLATE_ID
                        Template ID to use when multiple templates exist in the file.
  --variables VARIABLES
                        JSON string of variables to pass to the template.
  --variables-file VARIABLES_FILE
                        JSON file of variables to pass to the template.
  --model MODEL         The model to use for the query (e.g., gpt-4).
  --max-tokens MAX_TOKENS
                        Maximum number of tokens for the response (default: 8192).
  --max-length MAX_LENGTH
                        Maximum character length for the prompt (default: 2048).
  --api-key API_KEY     API key for the selected provider. If not provided, the environment variable for the provider will be used.
```

```bash
$ llmquery --provider OPENAI --template ./llmquery-templates/chat-template.yaml \
  --variables '{"user_input": "What is AI?"}' --api-key your-api-key --model gpt-4
```

The `llmquery` CLI  provides a command-line interface for interacting with Language Model APIs. The tool simplifies querying large language models by using YAML templates. This can used for various applications such as automation, testing, and scripting.

---

## Running the CLI

The `llmquery` binary is executed from the command line and supports various options for customization and configuration. Below is a detailed breakdown of its options and usage patterns.

---

## Command-Line Options

### General Options

- `--provider`
  - **Description**: Specifies the LLM provider to use.
  - **Accepted Values**: `OPENAI`, `ANTHROPIC`, `GOOGLE_GEMINI`, `OLLAMA`
  - **Example**: `--provider OPENAI`

- `--templates-path`
  - **Description**: Path to the directory containing YAML templates.
  - **Default**: Set by the `llmquery` framework.
  - **Example**: `--templates-path ./llmquery-templates`

- `--template-id`
  - **Description**: Specifies a template ID for cases with multiple templates.
  - **Example**: `--template-id general-query`

- `--variables`
  - **Description**: JSON string defining variables to pass to the selected template.
  - **Example**: `--variables '{"user_input": "Hello"}'`

- `--variables-file`
  - **Description**: Path to a JSON file containing variables for the template.
  - **Example**: `--variables-file ./variables.json`

### Model and API Options

- `--model`
  - **Description**: Specifies the model to query.
  - **Default**: Set by the `LLMQUERY_MODEL` environment variable.
  - **Example**: `--model gpt-4`

- `--max-tokens`
  - **Description**: Maximum number of tokens for the response.
  - **Default**: `8192`
  - **Example**: `--max-tokens 2048`

- `--max-length`
  - **Description**: Maximum character length for the prompt.
  - **Default**: `2048`
  - **Example**: `--max-length 1024`

- `--api-key`
  - **Description**: API key for the specified provider.
  - **Note**: If omitted, the relevant environment variable will be used.

---

## Examples

```bash
llmquery --provider OPENAI --templates-path ./llmquery-templates \
  --template-id basic-query --variables '{"user_input": "What is AI?"}' \
  --api-key YOUR_API_KEY --model gpt-4
```

### Using Variables from a File

```bash
llmquery --provider ANTHROPIC --templates-path ./llmquery-templates \
  --template-id basic-query --variables-file ./vars.json \
  --api-key YOUR_API_KEY --model claude-3-5-sonnet-latest
```

### Setting Maximum Tokens

```bash
llmquery --provider GOOGLE_GEMINI --templates-path ./llmquery-templates \
  --template-id translate-task --variables '{"text": "Hello", "language": "French"}' \
  --api-key YOUR_API_KEY --model gemini-latest --max-tokens 1000
```


---

# 🧩 Integration Examples

## Use Case: Static Code Analysis with LLMs

```python

code = """
def index
  @users = User.where("name LIKE '%#{params[:search]}%'") if params[:search].present?
  @users ||= User.all
end
"""
query = LLMQuery(
    provider="ANTHROPIC",
    templates_path=llmquery.TEMPLATES_PATH,
    template_id="detect-security-vulnerabilities"
    variables={"code": code},
    anthropic_api_key="your-api-key",
    model="claude-3-5-sonnet-latest"
)

print(query.Query())
```

## Use Case: PR Summary

```python

diff = """diff --git a/example.py b/example.py
+ def secure_function(password):
+     hashed_password = hash_password(password)
+     log("Password successfully hashed")
+
+ user_password = get_password_from_user()
+ secure_function(user_password)
"""
query = LLMQuery(
    provider="GOOGLE_GEMINI",
    templates_path=llmquery.templates_path,
    template_id="pr-summary-generator",
    variables={"diff": diff},
    google_gemini_api_key="your-api-key",
    model="gemini-1.5-flash"
)

print(query.Query())
```
# ⚙️ Environment Variables


- `OPENAI_API_KEY`
  - **Description**: API key for the OpenAI provider.
  - **Example**: `export OPENAI_API_KEY="API_KEY"`

- `ANTHROPIC_API_KEY`
  - **Description**: API key for the Anthropic provider.
  - **Example**: `export ANTHROPIC_API_KEY="API_KEY"`

- `GOOGLE_GEMINI_API_KEY`
  - **Description**: API key for the Google Gemini provider.
  - **Example**: `export GOOGLE_GEMINI_API_KEY="API_KEY"`
  -
- Check the full list of environment variables at `example.env`.


---

# 📝 Templates

`llmquery` has a collection of well-tested LLM Prompts Templates for various use-cases, including Application Security, AI Security, Code Reviews, Developer Velocity, and general cases. You can check the templates at the `./llmquery-templates` directory. All templates are bundled within llmquery, and can be accessed directly when refrencing the template ID.


Templates are powered by Jinja2, a Turing-complete template engine. This allows for the creation of dynamic and flexible templates through the use of conditional statements, loops, functions, and other advanced constructs.


View the full templates documentation at the [llmquery templates documentation](https://github.com/mazen160/llmquery/blob/master/docs/templates.md).

---

# ✨ Want to Contribute?

We’re always looking for contributions! Here are some ideas to get started:

- Add support for new LLM providers.
- Develop new YAML templates for common use cases.
- Improve error handling and validation logic.
- Build additional examples and documentation.
- Design a web interface for managing queries and responses.

Feel free to create issues, submit pull requests, or suggest enhancements on GitHub.

---


# 📄 License

This project is licensed under the MIT License.

---

# 💚 Author

**Mazin Ahmed**

- **Website**: [https://mazinahmed.net](https://mazinahmed.net)
- **Email**: [mazin@mazinahmed.net](mailto:mazin@mazinahmed.net)
- **Twitter**: [https://twitter.com/mazen160](https://twitter.com/mazen160)
- **LinkedIn**: [http://linkedin.com/in/infosecmazinahmed](http://linkedin.com/in/infosecmazinahmed)
