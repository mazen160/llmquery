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

ACCEPTED_PROVIDERS = ["OPENAI", "ANTHROPIC", "GOOGLE_GEMINI", "OLLAMA"]
TEMPLATES_PATH = os.path.join(sys.prefix, 'llmquery-templates')

def find_templates_path():
    possible_paths = [
                      os.path.join(sys.prefix, 'share', 'llmquery-templates'),
                      os.path.join(sys.prefix, 'share', 'llmquery', 'llmquery-templates'),
                      os.path.realpath(os.path.join(path, "llmquery-templates")),
                      os.path.realpath(os.path.join(path, "templates"))
    ]

    if os.path.exists(TEMPLATES_PATH):
        return TEMPLATES_PATH
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return None

TEMPLATES_PATH = find_templates_path()

class LLMQuery(object):
    def __init__(self,
                 provider: str = None,
                 template_inline: str = None,
                 templates_path: str = None,
                 template_id: str = None,
                 variables: dict = None,
                 openai_api_key: str = None,
                 anthropic_api_key: str = None,
                 google_gemini_api_key: str = None,
                 model: str = None,
                 max_tokens: int = 8192,
                 max_length: int = 2048):
        self.template = None
        provider = provider.upper()
        if provider not in ACCEPTED_PROVIDERS:
            raise ValueError(f"Provider '{provider}' is not supported.")
        self.provider = provider

        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        self.google_gemini_api_key = google_gemini_api_key
        self.model = model

        if template_inline and templates_path:
            raise ValueError("You cannot specify both 'template_inline' and 'templates_path' parameters.")

        if not template_inline and not templates_path:
            raise ValueError("You must specify either 'template_inline' or 'templates_path' parameter.")
        if template_inline:
            self.template = template_inline
            self.template = parser.Template(inline=self.template, variables=variables)

        if type(variables) is not dict:
            raise ValueError("The 'variables' parameter must be a dictionary.")
        self.variables = variables

        if templates_path:
            self.templates = parser.load_templates(templates_path)
            self.templates = parser.filter_invalid_templates(self.templates, variables=self.variables)

        if len(self.templates) == 1:
            self.template = self.templates[0]

        if len(self.templates) > 1 and not template_id:
            raise ValueError("Multiple templates found. You must specify a 'template_id' parameter.")

        if template_id:
            for t in self.templates:
                if t.id == template_id:
                    self.template = t
                    break
        if not self.template:
            raise ValueError("Template not found.")

        self.prompt_tokens = parser.get_prompt_tokens_count(self.template.rendered_prompt)
        self.system_prompt_tokens = parser.get_prompt_tokens_count(self.template.rendered_system_prompt)
        self.total_tokens = self.prompt_tokens + self.system_prompt_tokens
        if self.total_tokens > max_tokens:
            raise ValueError(f"Total tokens ({self.total_tokens}) exceed the maximum tokens allowed ({max_tokens}).")

        self.total_length = len(self.template.rendered_prompt) + len(self.template.rendered_system_prompt)
        if self.total_length > max_length:
            raise ValueError(f"Total length ({self.total_length}) exceed the maximum length allowed ({max_length}).")

    def set_variables(self, variables):
        self.variables.update(variables)

    def Query(self):
        if self.provider == "OPENAI":
            return openai.openai_chat_completion(openai_api_key=self.openai_api_key,
                                                 model=self.model,
                                                 system_prompt=self.template.rendered_system_prompt,
                                                 user_prompt=self.template.rendered_prompt)
        elif self.provider == "ANTHROPIC":
            return anthropic_claude.anthropic_cluade_message(anthropic_api_key=self.anthropic_api_key,
                                                             model=self.model,
                                                             system_prompt=self.template.rendered_system_prompt,
                                                             user_prompt=self.template.rendered_prompt)
        elif self.provider == "GOOGLE_GEMINI":
            return google_gemini.google_gemini_generate_content(url_endpoint=None,
                                                                google_gemini_api_key=self.google_gemini_api_key,
                                                                model=self.model,
                                                                system_prompt=self.template.rendered_system_prompt,
                                                                user_prompt=self.template.rendered_prompt)
        elif self.provider == "OLLAMA":
            return ollama.ollama_generate_content(url_endpoint=None,
                                                  model=self.model,
                                                  system_prompt=self.template.rendered_system_prompt,
                                                  user_prompt=self.template.rendered_prompt)
        else:
            raise ValueError("Provider not supported.")
