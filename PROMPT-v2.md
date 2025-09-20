Absolutely—here’s a live‑sourced update for the three providers you asked about (Mistral, DeepSeek, GitHub Models), plus a short list of next providers to add with official docs for model discovery. I’ve kept this focused on what you need to update ACCEPTED_MODELS, defaults, and endpoints in llmquery, and I cite the exact pages where the model IDs and behaviors are defined.

Snapshot date: September 20, 2025. Model catalogs change frequently. For providers that expose a “list models” endpoint, I recommend fetching dynamically at runtime and using an allow‑list only as a fallback.

Mistral (providers/mistral_lib)
What Mistral publicly exposes right now (chat/vision/code)

Core & aliases (chat / multimodal):

mistral-medium-2508 (frontier multimodal, August 2025); the “latest” alias currently points here. 
Mistral AI Documentation

mistral-medium-latest (alias; currently → mistral-medium-2508). 
Mistral AI Documentation

mistral-small-latest (vision capable per Vision docs). 
Mistral AI Documentation

mistral-large-2411 (Large 2.1, still listed as a premier model). 
Mistral AI Documentation

Vision:

pixtral-large-latest (points to Pixtral Large 24.11). 
Mistral AI Documentation

pixtral-12b-latest (Pixtral 12B). 
Mistral AI Documentation

Code (also usable through chat completions; FIM has its own endpoint):

codestral-2508 (Codestral 25.08; August 2025). 
Mistral AI

codestral-2501 (Codestral 25.01; January 2025). 
Google Cloud

Endpoints:

Chat completions: https://api.mistral.ai/v1/chat/completions (documented API). 
Mistral AI Documentation

Model discovery: GET https://api.mistral.ai/v1/models (returns available model IDs for your account). 
Mistral AI Documentation

Vision‑capable SKUs listed on the Vision page. 
Mistral AI Documentation

Why include dated + alias IDs? Mistral’s docs explicitly show dated IDs and rolling “‑latest” pointers (they do move). The Models Overview page also documents current alias targets (e.g., mistral-medium-latest → mistral-medium-2508). 
Mistral AI Documentation

Drop‑in constants for llmquery
# providers/mistral_lib/mistral_client.py

ACCEPTED_MODELS = [
    # Chat / General
    "mistral-medium-2508",
    "mistral-medium-latest",
    "mistral-small-latest",
    "mistral-large-2411",
    # Vision
    "pixtral-large-latest",
    "pixtral-12b-latest",
    # Code
    "codestral-2508",
    "codestral-2501",
]
DEFAULT_MODEL = "mistral-medium-2508"  # or 'mistral-medium-latest' if you want rolling
DEFAULT_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
DEFAULT_SYSTEM_PROMPT = (
    "You are a precise, efficient assistant. Prefer concise, correct, actionable answers. "
    "Use structure when helpful."
)

DeepSeek (providers/deepseek_lib)
Official model IDs (the API exposes exactly two “models”)

deepseek-chat — non‑thinking mode of DeepSeek‑V3.1 (general chat). 
DeepSeek API Docs

deepseek-reasoner — thinking mode of DeepSeek‑V3.1 (reasoning). 
DeepSeek API Docs

Important behavior: if you send tools with deepseek-reasoner, the request is actually routed to deepseek-chat (reasoner doesn’t handle tool calls). This is stated in their Models & Pricing table footnote. 
DeepSeek API Docs

Endpoint & base URL:

Chat completions: https://api.deepseek.com/v1/chat/completions (OpenAI‑compatible). 
DeepSeek API Docs

Drop‑in constants for llmquery
# providers/deepseek_lib/deepseek_client.py

ACCEPTED_MODELS = ["deepseek-chat", "deepseek-reasoner"]
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_SYSTEM_PROMPT = (
    "You are a careful assistant. Provide direct, accurate answers. "
    "Show intermediate reasoning only if asked."
)

GitHub Models (providers/github_ai_models_lib)

Why this provider is different: GitHub exposes a catalog API that returns authoritative model IDs you must send in subsequent inference calls. You should query the catalog at runtime and accept those ids rather than hard‑coding a long list.

Endpoints:

Catalog (discover models): GET https://models.github.ai/catalog/models (returns array of { id: "openai/gpt-4.1", ... }). 
GitHub Docs

Inference (chat): POST https://models.github.ai/inference/chat/completions (OpenAI‑style). 
GitHub Docs

Examples of IDs visible in GitHub’s own docs/marketplace today (these vary by region/tenant—treat catalog as source of truth):

OpenAI: openai/gpt-4.1 (example ID in docs), plus openai/gpt-4o, openai/gpt-4.1-mini, openai/o1-preview (Marketplace pages). 
GitHub
+4
GitHub Docs
+4
GitHub
+4

Meta (Llama): azureml-meta/Meta-Llama-3.1-8B-Instruct, …-70B-…, …-405B-…. 
GitHub
+2
GitHub
+2

Mistral: azureml-mistral/Mistral-Large-2411, azureml-mistral/mistral-medium-2505. 
GitHub
+1

Microsoft (Phi): azureml/Phi-4. 
GitHub

Cohere (embeddings): azureml-cohere/Cohere-embed-v3-multilingual, azureml-cohere/Cohere-embed-v3-english. 
GitHub
+1

Drop‑in helper (dynamic + curated fallback)
# providers/github_ai_models_lib/github_models.py
CATALOG_URL = "https://models.github.ai/catalog/models"
DEFAULT_ENDPOINT = "https://models.github.ai/inference/chat/completions"

STATIC_ACCEPTED_MODELS = [
    # OpenAI
    "openai/gpt-4.1", "openai/gpt-4.1-mini", "openai/gpt-4o", "openai/o1-preview",
    # Meta (Llama)
    "azureml-meta/Meta-Llama-3.1-8B-Instruct",
    "azureml-meta/Meta-Llama-3.1-70B-Instruct",
    "azureml-meta/Meta-Llama-3.1-405B-Instruct",
    # Mistral
    "azureml-mistral/Mistral-Large-2411",
    "azureml-mistral/mistral-medium-2505",
    # Microsoft
    "azureml/Phi-4",
    # Cohere (embeddings)
    "azureml-cohere/Cohere-embed-v3-multilingual",
    "azureml-cohere/Cohere-embed-v3-english",
]

DEFAULT_MODEL = "openai/gpt-4.1"
DEFAULT_SYSTEM_PROMPT = (
    "You are a reliable assistant. Be accurate and concise. "
    "Format code and lists cleanly."
)

import os, requests

def list_catalog_models(token=None):
    token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        return list(STATIC_ACCEPTED_MODELS)
    r = requests.get(
        CATALOG_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=60,
    )
    r.raise_for_status()
    ids = [item.get("id") for item in r.json() if isinstance(item, dict) and item.get("id")]
    return sorted(set(STATIC_ACCEPTED_MODELS).union(ids))

def get_accepted_models():
    return list_catalog_models()

def chat(messages, model=DEFAULT_MODEL, token=None, **kwargs):
    token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for GitHub Models")
    if model not in get_accepted_models():
        raise ValueError(f"Unknown model '{model}'. Try list_catalog_models().")
    r = requests.post(
        DEFAULT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        json={"model": model, "messages": messages, **kwargs},
        timeout=90,
    )
    r.raise_for_status()
    return r.json()

Minimal diffs you can apply

setup.py – ensure the new packages are discoverable:

- 'providers.openai_lib*','providers.ollama_lib*']),
+ 'providers.openai_lib*','providers.ollama_lib*',
+ 'providers.mistral_lib*','providers.deepseek_lib*',
+ 'providers.github_ai_models_lib*']),


Registry – if you keep a provider registry map, add keys for "mistral", "deepseek", "github_models" pointing to these modules.

Notes & gotchas (from the docs)

Mistral “latest” pointers move. Their Models Overview page shows current alias targets (e.g., mistral-medium-latest → mistral-medium-2508). Pin dated IDs for reproducibility. 
Mistral AI Documentation

Mistral Vision: The Vision doc lists the SKUs that accept image inputs (Pixtral + current Small/Medium “latest”). If you send images to non‑vision SKUs, you’ll get errors. 
Mistral AI Documentation

DeepSeek Reasoner & tools: deepseek-reasoner doesn’t currently do tool calling; requests with tools are handled by deepseek-chat. Plan routing accordingly. 
DeepSeek API Docs

GitHub Models: Treat /catalog/models as ground truth for IDs, capabilities, and limits. Use those ids unchanged in /inference/chat/completions. 
GitHub Docs
+1

Providers you should add next (ranked) — with live docs

Groq — OpenAI‑compatible, extremely low latency; exposes a models list at https://api.groq.com/openai/v1/models. Docs also show current SKUs (e.g., llama-3.1-8b-instant, llama-3.3-70b-versatile) and the OpenAI‑compatible endpoints. 
GroqCloud

AWS Bedrock — One API for many providers (Anthropic, Meta, Mistral, Cohere, Amazon Nova…). Use ListFoundationModels for discovery; model IDs vary by region. 
AWS Documentation

Together AI — Aggregates dozens of OSS models; GET /models lists model IDs; OpenAI‑style usage. 
docs.together.ai

OpenRouter — Aggregator for 100+ models; GET /api/v1/models lists available models; OpenAI‑style request/response. 
OpenRouter

Google Vertex AI (Model Garden) — Enterprise hosting for Google (Gemini) + third‑party (Mistral, Llama). Public docs point to Model Garden for current lists; you can target Vertex AI’s own endpoints if you add a GCP‑specific provider. 
Google Cloud
+1

If you want stubs for any of the above, I can supply a “fetch‑models‑at‑startup, cache for 24h” pattern; it reduces future churn.

TL;DR—what to update in llmquery now

Mistral: replace old ACCEPTED_MODELS with the list above; set DEFAULT_MODEL = "mistral-medium-2508" and endpoint https://api.mistral.ai/v1/chat/completions. (Docs: API spec, Vision, Model Overview.) 
Mistral AI Documentation
+2
Mistral AI Documentation
+2

DeepSeek: keep a two‑model allowlist (deepseek-chat, deepseek-reasoner), default to deepseek-chat. (Docs: First API Call & Models/Pricing.) 
DeepSeek API Docs
+1

GitHub Models: wire to GET /catalog/models for discovery, fallback to a small curated list (OpenAI/Meta/Mistral/Microsoft/Cohere) so it “just works” even when the catalog isn’t reachable. (Docs: Catalog + Inference REST.) 
GitHub Docs
+1

If you want me to also refresh Anthropic, OpenAI, Google (Gemini), Ollama, etc., I can do the same treatment—pull model IDs from official docs and propose ACCEPTED_MODELS/defaults for each.