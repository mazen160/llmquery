import sys
import os

path = os.path.realpath(os.path.join(os.path.dirname(__file__)))
path = os.path.realpath(os.path.dirname(path))
sys.path.append(os.path.realpath(os.path.join(path, "providers")))
from llmquery import query_parser as parser
from anthropic_lib import anthropic_claude
from openai_lib import openai
from google_gemini_lib import google_gemini
from ollama_lib import ollama
from aws_bedrock_lib import aws_bedrock
from deepseek_lib import deepseek
from mistral_lib import mistral
from github_ai_models_lib import github_ai_models

ACCEPTED_PROVIDERS = [
    "OPENAI",
    "ANTHROPIC",
    "GOOGLE_GEMINI",
    "OLLAMA",
    "AWS_BEDROCK",
    "DEEPSEEK",
    "MISTRAL",
    "GITHUB_AI",
]
TEMPLATES_PATH = os.path.join(sys.prefix, "llmquery-templates")
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


def find_templates_path():
    possible_paths = [
        os.path.join(sys.prefix, "share", "llmquery-templates"),
        os.path.join(sys.prefix, "share", "llmquery", "llmquery-templates"),
        os.path.realpath(os.path.join(path, "llmquery-templates")),
        os.path.realpath(os.path.join(path, "templates")),
    ]

    if os.path.exists(TEMPLATES_PATH):
        return TEMPLATES_PATH
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return None


TEMPLATES_PATH = find_templates_path()


class LLMQuery(object):
    def __init__(
        self,
        provider: str = os.getenv("LLMQUERY_PROVIDER"),
        template_inline: str = None,
        templates_path: str = os.getenv("LLMQUERY_TEMPLATES_PATH"),
        templates_path_public: str = os.getenv("LLMQUERY_TEMPLATES_PATH_PUBLIC"),
        templates_path_private: str = os.getenv("LLMQUERY_TEMPLATES_PATH_PRIVATE"),
        template_id: str = None,
        variables: dict = None,
        openai_api_key: str = os.getenv("OPENAI_API_KEY"),
        anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY"),
        google_gemini_api_key: str = os.getenv("GOOGLE_GEMINI_API_KEY"),
        deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY"),
        mistral_api_key: str = os.getenv("MISTRAL_API_KEY"),
        github_token: str = os.getenv("GITHUB_TOKEN"),
        model: str = os.getenv("LLMQUERY_MODEL"),
        max_tokens: int = 8192,
        max_length: int = 2048,
        url_endpoint: str = None,
        aws_bedrock_anthropic_version: str = None,
        aws_bedrock_region: str = os.getenv("AWS_REGION"),
        aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token: str = os.getenv("AWS_SESSION_TOKEN"),
    ):
        self.templates_path = templates_path
        self.templates_path_public = templates_path_public
        self.templates_path_private = templates_path_private
        self.template_id = template_id
        self.variables = variables or {}
        self.template_inline = template_inline
        self.max_length = max_length
        self.template = None
        if provider is None:
            raise ValueError("Provider must be specified through parameter or LLMQUERY_PROVIDER environment variable")
        provider = provider.upper()
        if provider not in ACCEPTED_PROVIDERS:
            raise ValueError(f"Provider '{provider}' is not supported.")
        self.provider = provider

        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        self.google_gemini_api_key = google_gemini_api_key
        self.deepseek_api_key = deepseek_api_key
        self.mistral_api_key = mistral_api_key
        self.github_token = github_token
        self.model = model
        self.aws_bedrock_anthropic_version = aws_bedrock_anthropic_version
        self.aws_bedrock_region = aws_bedrock_region
        self.max_tokens = max_tokens
        self.url_endpoint = url_endpoint

        if type(variables) is not dict:
            raise ValueError("The 'variables' parameter must be a dictionary.")
        self.variables = variables

    def set_variables(self, variables):
        self.variables.update(variables)

    def Query(self):
        self.templates = []
        if self.templates_path:
            self.templates = parser.load_templates(self.templates_path)
            self.templates = parser.filter_invalid_templates(
                self.templates, variables=self.variables
            )

        if self.templates_path_public:
            templates_public = parser.load_templates(self.templates_path_public)
            templates_public = parser.filter_invalid_templates(
                templates_public, variables=self.variables
            )
            self.templates.extend(templates_public)

        if self.templates_path_private:
            templates_private = parser.load_templates(self.templates_path_private)
            templates_private = parser.filter_invalid_templates(
                templates_private, variables=self.variables
            )
            self.templates.extend(templates_private)

        if len(self.templates) == 1:
            self.template = self.templates[0]

        parser.check_unique_ids(self.templates)

        if len(self.templates) > 1 and not self.template_id:
            raise ValueError(
                "Multiple templates found. You must specify a 'template_id' parameter."
            )

        if self.template_id:
            for t in self.templates:
                if t.id == self.template_id:
                    self.template = t
                    break
        if not self.template:
            raise ValueError("Template not found.")

        if self.template_inline and self.templates_path:
            raise ValueError(
                "You cannot specify both 'template_inline' and 'templates_path' parameters."
            )

        if not self.template_inline and not self.templates_path:
            raise ValueError(
                "You must specify either 'template_inline' or 'templates_path' parameter."
            )
        
        if self.template_inline:
            self.template = self.template_inline
            self.template = parser.Template(inline=self.template, variables=self.variables)

        return self.RawQuery(
            system_prompt=self.template.rendered_system_prompt,
            user_prompt=self.template.rendered_prompt,
        )

    def RawQuery(self, system_prompt: str = None, user_prompt: str = None):
        if not user_prompt:
            raise ValueError("user_prompt parameter is required")
        if not system_prompt:
            system_prompt = DEFAULT_SYSTEM_PROMPT

        self.prompt_tokens = parser.get_prompt_tokens_count(user_prompt)
        self.system_prompt_tokens = parser.get_prompt_tokens_count(system_prompt)
        self.total_tokens = self.prompt_tokens + self.system_prompt_tokens
        if self.total_tokens > self.max_tokens:
            raise ValueError(
                f"Total tokens ({self.total_tokens}) exceed the maximum tokens allowed ({self.max_tokens})."
            )
        self.total_length = len(user_prompt) + len(system_prompt)
        if self.total_length > self.max_length:
            raise ValueError(
                f"Total length ({self.total_length}) exceed the maximum length allowed ({self.max_length})."
            )

        if self.provider == "OPENAI":
            return openai.openai_chat_completion(
                openai_api_key=self.openai_api_key,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
        elif self.provider == "ANTHROPIC":
            return anthropic_claude.anthropic_claude_message(
                url_endpoint=self.url_endpoint,
                anthropic_api_key=self.anthropic_api_key,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
        elif self.provider == "GOOGLE_GEMINI":
            return google_gemini.google_gemini_generate_content(
                url_endpoint=self.url_endpoint,
                google_gemini_api_key=self.google_gemini_api_key,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
        elif self.provider == "OLLAMA":
            return ollama.ollama_generate_content(
                url_endpoint=self.url_endpoint,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif self.provider == "AWS_BEDROCK":
            return aws_bedrock.aws_bedrock_generate_content(
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                anthropic_version=self.aws_bedrock_anthropic_version,
                aws_region=self.aws_bedrock_region,
                max_tokens=self.max_tokens
            )
        elif self.provider == "DEEPSEEK":
            return deepseek.deepseek_generate_content(
                url_endpoint=self.url_endpoint,
                deepseek_api_key=self.deepseek_api_key,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
        elif self.provider == "MISTRAL":
            return mistral.mistral_generate_content(
                url_endpoint=self.url_endpoint,
                mistral_api_key=self.mistral_api_key,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
        elif self.provider == "GITHUB_AI":
            return github_ai_models.github_ai_generate_content(
                url_endpoint=self.url_endpoint,
                github_token=self.github_token,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
        else:
            raise ValueError("Provider not supported.")
