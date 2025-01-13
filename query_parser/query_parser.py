import pathlib
import yaml
import jinja2
from jinja2 import meta
import json
import tiktoken

DEFAULT_SYSTEM_PROMPT = """
You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value.
""".strip()


def read_file(p: str):
    with open(p, "r") as f:
        return f.read()


def render_template(template, variables):
    env = jinja2.Environment()
    parsed_content = env.parse(template)
    required_keys = meta.find_undeclared_variables(parsed_content)

    missing_keys = [key for key in required_keys if key not in variables]

    if missing_keys:
        raise Exception(f"Missing required keys: {missing_keys}")

    # Render the template
    compiled_template = env.from_string(template)
    return compiled_template.render(variables)


class Template(object):
    def __init__(self, path: str = None, inline: str = None, variables: dict = None):
        if inline and path:
            raise ValueError("You cannot specify both 'path' and 'inline' parameters.")
        if not inline and not path:
            raise ValueError("You must specify either 'path' or 'inline' parameter.")
        if path:
            self.path = path
            self.content = read_file(path)
        if inline:
            self.content = inline
        self.data = self.__parse_template()

        try:
            self.id = self.data["id"]
        except KeyError:
            raise KeyError("The 'id' field is missing in the template YAML file.")

        try:
            self.prompt = self.data["prompt"]
        except KeyError:
            raise KeyError("The 'prompt' field is missing in the template YAML file.")

        self.variables = self.data.get("variables", {})
        if variables:
            self.variables.update(variables)

        self.system_prompt = self.data.get("system_prompt", DEFAULT_SYSTEM_PROMPT)

        self.rendered_prompt = render_template(self.prompt, self.variables)
        self.rendered_system_prompt = render_template(self.system_prompt, self.variables)

        if not self.rendered_prompt:
            raise ValueError(f"Prompt is empty in template '{self.id}'")

        if not self.rendered_system_prompt:
            raise ValueError(f"System prompt is empty in template '{self.id}'. DEFAULT_SYSTEM_PROMPT was not used.")

    def __parse_template(self):
        return yaml.safe_load(self.content)


def load_templates(path: str):
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Path '{path}' does not exist.")

    if p.is_dir():
        return [str(x) for x in p.rglob("*") if x.is_file()]
    else:
        # Handle glob patterns
        return [str(x) for x in p.parent.glob(p.name) if x.is_file()]


def filter_invalid_templates(templates, variables={}):
    filtered_templates = []
    for t in templates:
        try:
            ok = Template(t, variables=variables)
            filtered_templates.append(ok)
        except Exception as e:
            print(f"Error: {t} - {e}")
    return filtered_templates


def extract_json(text):
    start = end = 0
    for i in range(len(text)):
        if text[i] == "{":
            start = i
            break
    for i in range(len(text) - 1, 0, -1):
        if text[i] == "}":
            end = i
            break

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def get_prompt_tokens_count(prompt: str, encoding: str = "o200k_base"):
    enc = tiktoken.get_encoding(encoding)
    num_tokens = len(enc.encode(prompt))
    return num_tokens