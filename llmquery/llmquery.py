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
        aws_bedrock_anthropic_version: str = None,
        aws_bedrock_region: str = os.getenv("AWS_REGION"),
        aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token: str = os.getenv("AWS_SESSION_TOKEN"),
    ):
        self.template = None
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

        if template_inline and templates_path:
            raise ValueError(
                "You cannot specify both 'template_inline' and 'templates_path' parameters."
            )

        if not template_inline and not templates_path:
            raise ValueError(
                "You must specify either 'template_inline' or 'templates_path' parameter."
            )
        if template_inline:
            self.template = template_inline
            self.template = parser.Template(inline=self.template, variables=variables)

        if type(variables) is not dict:
            raise ValueError("The 'variables' parameter must be a dictionary.")
        self.variables = variables

        if templates_path:
            self.templates = parser.load_templates(templates_path)
            self.templates = parser.filter_invalid_templates(
                self.templates, variables=self.variables
            )

        if templates_path_public:
            templates_public = parser.load_templates(templates_path_public)
            templates_public = parser.filter_invalid_templates(
                templates_public, variables=self.variables
            )
            self.templates.extend(templates_public)

        if templates_path_private:
            templates_private = parser.load_templates(templates_path_private)
            templates_private = parser.filter_invalid_templates(
                templates_private, variables=self.variables
            )
            self.templates.extend(templates_private)

        if len(self.templates) == 1:
            self.template = self.templates[0]

        parser.check_unique_ids(self.templates)

        if len(self.templates) > 1 and not template_id:
            raise ValueError(
                "Multiple templates found. You must specify a 'template_id' parameter."
            )

        if template_id:
            for t in self.templates:
                if t.id == template_id:
                    self.template = t
                    break
        if not self.template:
            raise ValueError("Template not found.")

        self.prompt_tokens = parser.get_prompt_tokens_count(
            self.template.rendered_prompt
        )
        self.system_prompt_tokens = parser.get_prompt_tokens_count(
            self.template.rendered_system_prompt
        )
        self.total_tokens = self.prompt_tokens + self.system_prompt_tokens
        if self.total_tokens > max_tokens:
            raise ValueError(
                f"Total tokens ({self.total_tokens}) exceed the maximum tokens allowed ({max_tokens})."
            )

        self.total_length = len(self.template.rendered_prompt) + len(
            self.template.rendered_system_prompt
        )
        if self.total_length > max_length:
            raise ValueError(
                f"Total length ({self.total_length}) exceed the maximum length allowed ({max_length})."
            )

    def set_variables(self, variables):
        self.variables.update(variables)

    def Query(self):
        """Execute the query using the processed template"""
        return self.raw_query(
            system_prompt=self.template.rendered_system_prompt,
            user_prompt=self.template.rendered_prompt
        )

    def raw_query(
        self,
        system_prompt: str = None,
        user_prompt: str = None,
        provider: str = None,
        model: str = None,
        max_tokens: int = None
    ):
        """Direct query execution without template processing"""
        # Use instance values as defaults if not provided
        provider = provider or self.provider
        model = model or self.model
        max_tokens = max_tokens or self.max_tokens

        # Validation
        if not user_prompt:
            raise ValueError("user_prompt parameter is required")

        # Calculate token usage
        prompt_tokens = parser.get_prompt_tokens_count(user_prompt)
        system_prompt_tokens = parser.get_prompt_tokens_count(system_prompt or "")
        total_tokens = prompt_tokens + system_prompt_tokens
        
        if total_tokens > max_tokens:
            raise ValueError(
                f"Total tokens ({total_tokens}) exceed maximum allowed ({max_tokens})"
            )

        # Provider dispatch
        if provider == "OPENAI":
            return openai.openai_chat_completion(
                openai_api_key=self.openai_api_key,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif provider == "ANTHROPIC":
            return anthropic_claude.anthropic_cluade_message(
                anthropic_api_key=self.anthropic_api_key,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif provider == "GOOGLE_GEMINI":
            return google_gemini.google_gemini_generate_content(
                url_endpoint=None,
                google_gemini_api_key=self.google_gemini_api_key,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif provider == "OLLAMA":
            return ollama.ollama_generate_content(
                url_endpoint=None,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif provider == "AWS_BEDROCK":
            return aws_bedrock.aws_bedrock_generate_content(
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                anthropic_version=self.aws_bedrock_anthropic_version,
                aws_region=self.aws_bedrock_region,
                max_tokens=max_tokens,
            )
        elif provider == "DEEPSEEK":
            return deepseek.deepseek_generate_content(
                deepseek_api_key=self.deepseek_api_key,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif provider == "MISTRAL":
            return mistral.mistral_generate_content(
                mistral_api_key=self.mistral_api_key,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        elif provider == "GITHUB_AI" or provider == "GITHUB_AI_MODELS":
            return github_ai_models.github_ai_generate_content(
                github_token=self.github_token,
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        else:
            raise ValueError("Provider not supported.")
