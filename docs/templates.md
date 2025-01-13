# YAML Templates for llmquery

This document serves as a guide for creating YAML templates for `llmquery`. Templates are the foundation of how prompts are structured, validated, and rendered for various Language Model APIs.

Templates are powered by Jinja2, a Turing-complete template engine. This allows for the creation of dynamic and flexible templates through the use of conditional statements, loops, functions, and other advanced constructs.

---

## Structure of a YAML Template

Each YAML template consists of the following key components:

### 1. **Template ID**

Every template must have a unique identifier specified under the `id` key.

```yaml
id: unique-template-id
```

### 2. **Template Metadata**

Metadata allows users to add descriptive information about their templates. It provides context, notes, or categorization for better organization.

#### Common Metadata Fields

```yaml
metadata:
    author: "Your Name"
    tags:
      - tag1
      - tag2
    category: "Your Category"
    description: "Your template description"
```

### 3. **System Prompt**

The `system_prompt` defines the behavior and tone of the LLM. This field describes the context and rules the model should follow.

```yaml
system_prompt: >
    You are a helpful assistant.
```

- Use `>` for multiline prompts.
- Keep instructions concise and explicit.

### 4. **Prompt**

The `prompt` field contains the main query or instruction sent to the model. Use variables to make the prompt dynamic.

```yaml
prompt: >
    Translate the following text from {{ source_language }} to {{ target_language }}:
    Text:
    {{ text }}
```

### 5. **Variables**

Variables allow the prompt to be dynamic and reusable. Define them under the `variables` key or pass them directly when instantiating the `LLMQuery` class. Variables provided in the `LLMQuery` class will overwrite those defined in the YAML template.

```yaml
variables:
    source_language: English
    target_language: Spanish
    text: "Hello, how are you?"
```

**Example of providing Variables in code:**

```python
from llmquery import LLMQuery

query = LLMQuery(
    provider="OPENAI",
    template_path="./templates/translate-natural-language.yaml",
    variables={"source_language": "French", "target_language": "German", "text": "Bonjour"},
    openai_api_key="your-api-key"
)
response = query.Query()
print(response)
```

---

## Example Templates

Here are some examples to help you create your own YAML templates.

### Example 1: Language Detection

```yaml
id: detect-natural-language

metadata:
    author: "Your Name"
    tags:
      - language-detection
    category: "Utility"

system_prompt: >
    You're an AI assistant. You should return the expected response without any additional information. The response should be exclusively in JSON with no additional code blocks or text.

prompt: >
    Analyze the following text and identify its language:
    Return response as: {"detected_language": "LANGUAGE_NAME"}
    {{ text }}

variables:
    text: " السلام عليكم"
```

### Example 2: Find Book Author

```yaml
id: find-book-author-name

metadata:
    author: "Your Name"
    tags:
      - book-info
    category: "Information Retrieval"

system_prompt: >
    You are an AI assistant that returns concise information in JSON format exclusively without any additional context, code blocks, or formatting.

prompt: >
    Who is the author of this book?
    Response should be in the format: {"author": "AUTHOR NAME"}
    Book name: {{ book }}

variables:
    book: Atomic Habits
```

### Example 3: Translation

```yaml
id: translate-natural-language

metadata:
    author: "Your Name"
    tags:
      - translation
      - language
    category: "Utility"

system_prompt: >
    You're an AI assistant. You should return the expected response without any additional information.

prompt: >
    Translate the following natural language from {{ source_language }} to {{ target_language }}:
    Text:

    {{ text }}

variables:
    source_language: English
    target_language: Spanish
    text: "Hello, how are you?"
```

---

## Grammar and Best Practices

### Grammar

1. **`id`**: Unique string identifying the template.
2. **`metadata`**: Optional descriptive information about the template.
3. **`system_prompt`**: Explicit instructions for the LLM.
4. **`prompt`**: The user instruction with variables embedded.
5. **`variables`**: Key-value pairs defining dynamic components of the prompt.

### Best Practices

1. **Clarity**: Keep prompts clear and concise.
2. **JSON Responses**: When applicable, enforce JSON-only outputs for structured responses.
3. **Error Handling**: Provide explicit instructions in the `system_prompt` to handle errors gracefully.
4. **Dynamic Variables**: Use variables to make the template reusable across different inputs.
5. **Validation**: Test templates to ensure they produce the expected results.

---

## Creating Your Own Template

1. Start with the `id` section to uniquely identify your template.
2. Add a `metadata` section to describe your template.
3. Write a clear `system_prompt` to define the behavior of the model.
4. Craft a `prompt` with placeholders for dynamic inputs.
5. Define the `variables` with default values to test the template.

### Example Template Skeleton

```yaml
id: your-template-id

metadata:
    author: "Your Name"
    tags:
      - example-tag
    category: "Example Category"

system_prompt: >
    [Define the behavior of the LLM here.]

prompt: >
    [Write the main instruction or query here. Use {{ variable_name }} for placeholders.]

variables:
    variable_name: "default value"
```

---

## Contribute Your Templates

We welcome contributions to the `llmquery` repository! If you've created useful YAML templates, consider submitting it to help the community.

### Steps to Submit a Template

1. Fork the repository from [GitHub](https://github.com/mazen160/llmquery).
2. Create a branch for your template addition.
3. Add your template under the appropriate directory (e.g., `templates/`).
4. Test your template to ensure it works as expected.
5. Open a Pull Request (PR) with a clear description of your template and its use case.

Join us in building a library of powerful, reusable templates for everyone!

GitHub Link: [https://github.com/mazen160/llmquery](https://github.com/mazen160/llmquery)

