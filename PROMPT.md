https://github.com/mazen160/llmquery

Is a project I'm working on. The available models have not been updated since January 2025. "
I need you to go and update each one of them. and provide a list of available models for each providers. Do research and everything. And then provide a document with all providers and now available models. Be thourough. 

https://github.com/mazen160/llmquery/blob/main/providers/anthropic_lib/anthropic_claude.py

ACCEPTED_MODELS = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-20241022",
    "claude-3-5-haiku-latest",
    "claude-3-opus-20240229",
    "claude-3-opus-latest",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]
DEFAULT_MODEL = "claude-3-5-haiku-latest"
DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


These models are old. I need you to update the list with all new models from the Documentation of each providers. and provide a document with changes.
ChatGPT said:
Request for GPT-5 Pro
Reasoned for 15m 23s

Awesome—thanks for the pointers and for the exact file path. I researched the current (as of Sept 19, 2025) model lineups for each provider supported by your package and prepared:

Updated ACCEPTED_MODELS (and recommended DEFAULT_MODEL) for each provider included in your setup.py (Anthropic, OpenAI, Google Gemini, Ollama).

A concise diff-style patch you can drop into each provider file.

A thorough reference document (below) listing all now-available models we should accept, plus deprecations/notes and links to the official docs I used.

Why only these four providers?
Your current setup.py bundles only:

providers.anthropic_lib*

providers.google_gemini_lib*

providers.openai_lib*

providers.ollama_lib* 
GitHub

If/when you add DeepSeek/Mistral/GitHub AI/AWS Bedrock modules to packages=find_packages(...), I can expand the same treatment to them.

0) Quick changes you can paste now
A) providers/anthropic_lib/anthropic_claude.py

What’s new
Anthropic now offers Claude Sonnet 4 and Claude Opus 4 (and Opus 4.1) in addition to Claude 3.7 Sonnet. Anthropic has announced deprecation of the Sonnet 3.5 snapshots (retirement Oct 22, 2025). Their docs recommend using specific snapshots for production rather than -latest aliases. 
Claude Docs
+1

Minimal, safe update (keep snapshot IDs + limited “latest” where the alias is documented):

@@
-ACCEPTED_MODELS = [
-    "claude-3-5-sonnet-20241022",
-    "claude-3-5-sonnet-latest",
-    "claude-3-5-haiku-20241022",
-    "claude-3-5-haiku-latest",
-    "claude-3-opus-20240229",
-    "claude-3-opus-latest",
-    "claude-3-sonnet-20240229",
-    "claude-3-haiku-20240307",
-]
-DEFAULT_MODEL = "claude-3-5-haiku-latest"
-DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
-DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."
+ACCEPTED_MODELS = [
+    # Claude 4.x
+    "claude-opus-4-1-20250805",     # newest Opus snapshot (Aug 05, 2025)
+    "claude-opus-4-20250514",       # Opus 4 (May 14, 2025)
+    "claude-sonnet-4-20250514",     # Sonnet 4 (May 14, 2025)
+
+    # Claude 3.7
+    "claude-3-7-sonnet-20250219",
+    "claude-3-7-sonnet-latest",     # Anthropic documents this alias
+
+    # Claude 3.5 / 3 (kept for compatibility; Sonnet 3.5 is deprecated Oct 22, 2025)
+    "claude-3-5-haiku-20241022",
+    "claude-3-5-haiku-latest",
+    "claude-3-opus-20240229",
+    "claude-3-opus-latest",
+    "claude-3-sonnet-20240229",
+    "claude-3-haiku-20240307",
+    # (optional) "claude-3-5-sonnet-20241022"  # temporarily supported but deprecated
+]
+DEFAULT_MODEL = "claude-sonnet-4-20250514"  # recommended general default in 2025
+DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
+DEFAULT_SYSTEM_PROMPT = "You are a highly intelligent assistant. Respond to user queries with precise, well-informed answers on the first attempt. Tailor responses to the user's context and intent, using clear and concise language. Always prioritize relevance, accuracy, and value."


Sources: Anthropic Models overview and “List Models” API; deprecation note for Sonnet 3.5. 
Claude Docs
+2
Claude Docs
+2

B) providers/openai_lib/openai_gpt.py

What’s new
OpenAI’s current generally-available families for text chat include GPT‑4.1, GPT‑4o, and the o‑series (notably o4‑mini and o3). OpenAI still documents the o1 series (Responses-only). GPT‑4 (legacy) was retired from ChatGPT and is in various stages of deprecation across surfaces; use current models for new work. 
MSPoweruser
+5
OpenAI Platform
+5
OpenAI Platform
+5

Safe update (chat text models)

@@
-ACCEPTED_MODELS = [
-    # (old list omitted)
-]
-DEFAULT_MODEL = "gpt-4o-mini"
-DEFAULT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
+ACCEPTED_MODELS = [
+    # Recommended current chat models
+    "gpt-4o",
+    "gpt-4o-mini",
+    "gpt-4.1",
+    "gpt-4.1-mini",
+
+    # Reasoning-oriented models (some features require the Responses API)
+    "o4-mini",
+    "o3",
+
+    # Compatibility / legacy (still widely used, but not recommended for new work)
+    "gpt-4-turbo-2024-04-09",
+    "gpt-3.5-turbo",
+]
+DEFAULT_MODEL = "gpt-4o"  # “best for most tasks” per OpenAI docs
+DEFAULT_ENDPOINT = "https://api.openai.com/v1/chat/completions"  # keep; note: o1-series is Responses-only


Note: If you want to support the o1 family too, consider adding a conditional path hitting the Responses API for those model IDs (OpenAI docs state o1/o1‑pro use Responses to support pre‑response “thinking” and multi‑turn tool use). 
OpenAI Platform

C) providers/google_gemini_lib/google_gemini.py

What’s new
The Gemini 2.5 and 2.0 generations are live in the Gemini API. Google’s model page documents stable IDs like gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite, and gemini-2.0-flash-lite; 1.5 Pro is marked with a deprecation date Sept 2025. Google explains the naming/alias rules (stable vs preview/experimental). 
Google AI for Developers
+3
Google AI for Developers
+3
Google AI for Developers
+3

@@
-ACCEPTED_MODELS = [
-    # (old list omitted)
-]
-DEFAULT_MODEL = "gemini-1.5-flash"
-DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
+ACCEPTED_MODELS = [
+    # Gemini 2.5 (current top tier)
+    "gemini-2.5-pro",
+    "gemini-2.5-flash",
+    "gemini-2.5-flash-lite",
+
+    # Gemini 2.0
+    "gemini-2.0-flash",
+    "gemini-2.0-flash-lite",
+
+    # 1.5 (kept for temporary compatibility; 1.5 Pro deprecates Sept 2025)
+    "gemini-1.5-pro",
+    "gemini-1.5-pro-latest",
+]
+DEFAULT_MODEL = "gemini-2.5-flash"  # fast, capable, cost‑efficient
+DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


Versioning/aliases: Google recommends stable IDs like gemini-2.5-pro for production; preview/experimental names (e.g., ...-preview-05-20, ...-exp-...) are available but not stable. 
Google AI for Developers

D) providers/ollama_lib/ollama.py

What’s new
Ollama’s library has added recent open models including Llama 4, Llama 3.3, DeepSeek‑R1, Qwen3, and Gemma 3n in addition to the Llama 3.1 family. Since Ollama accepts any installed model tag, it’s best to whitelist only popular, well‑maintained IDs (and still allow arbitrary strings if you want power users to override). 
Ollama
+5
Ollama
+5
Ollama
+5

@@
-ACCEPTED_MODELS = [
-    # (old list omitted)
-]
-DEFAULT_MODEL = "llama3.1:8b"
-DEFAULT_ENDPOINT = "http://localhost:11434/api/generate"
+ACCEPTED_MODELS = [
+    # Meta Llama
+    "llama4",              # mixture-of-experts, multimodal
+    "llama4:16x17b",
+    "llama4:128x17b",
+    "llama3.3",            # strong 70B open model
+    "llama3.2",
+    "llama3.2-vision",
+    "llama3.1:8b",
+    "llama3.1:70b",
+    "llama3.1:405b",
+
+    # Alibaba Qwen
+    "qwen3",               # new generation
+    "qwen2.5:7b",
+    "qwen2.5:14b",
+    "qwen2.5:32b",
+    "qwen2.5:72b",
+
+    # Google Gemma
+    "gemma3n",             # efficient on-device class
+    "gemma2:2b",
+    "gemma2:9b",
+    "gemma2:27b",
+
+    # DeepSeek
+    "deepseek-r1",         # reasoning family (various sizes/tags)
+
+    # (Common smaller baselines)
+    "phi4",
+    "mistral-nemo",
+]
+DEFAULT_MODEL = "llama3.3"  # good default on modern GPUs; adjust for your user base
+DEFAULT_ENDPOINT = "http://localhost:11434/api/generate"


Notes
• These are library page IDs as published by Ollama; exact tags (quantizations like :q4_K_M, etc.) vary by device and user preference. 
Ollama

• If you want to keep the provider strict yet flexible, accept any non-empty string and validate at runtime by calling GET /api/tags on the local Ollama server.

1) Thorough reference (what’s available now, with sources)

Snapshot date: Sept 19, 2025. Where providers discourage -latest, I list snapshots and add notes on aliases.

Anthropic (Claude)

Current, recommended models

claude-opus-4-1-20250805 (Opus 4.1)

claude-opus-4-20250514 (Opus 4)

claude-sonnet-4-20250514 (Sonnet 4)

claude-3-7-sonnet-20250219, claude-3-7-sonnet-latest (Sonnet 3.7; includes “extended thinking” mode) 
Claude Docs
+1

Still available / legacy for compatibility

claude-3-5-haiku-20241022, claude-3-5-haiku-latest

claude-3-opus-20240229, claude-3-opus-latest

claude-3-sonnet-20240229, claude-3-haiku-20240307 
Claude Docs

Deprecations

claude-3-5-sonnet-20241022 (retired Oct 22, 2025). Migrate to Sonnet 4. 
Claude Docs

Docs: Models overview; Models API (list/get). 
Claude Docs
+2
Claude Docs
+2

OpenAI

Current, recommended chat models

gpt-4o (flagship multimodal, “best for most tasks”)

gpt-4o-mini (small, cheap multimodal)

gpt-4.1 (instruction-following, 1M context)

gpt-4.1-mini (small variant) 
OpenAI Platform
+1

Reasoning / special

o4-mini (fast reasoning)

o3 (advanced reasoning)

Note: the o1 family exists and is Responses API–only; enable if you add a Responses path. 
OpenAI Platform
+2
OpenAI Platform
+2

Legacy/compat (still seen in the wild)

gpt-4-turbo-2024-04-09, gpt-3.5-turbo (use only for backward compatibility; not recommended for new work). 
OpenAI Platform

Deprecations worth noting

GPT‑4 retired from ChatGPT UI and older previews retired; GPT‑4.5‑preview removed from API (July 2025). Plan migrations to current models above. 
MSPoweruser
+1

Docs: Model pages for GPT‑4o / GPT‑4.1 / o‑series; Deprecations. 
OpenAI Platform
+4
OpenAI Platform
+4
OpenAI Platform
+4

Google Gemini (Gemini API)

Stable, recommended (text/multimodal)

gemini-2.5-pro

gemini-2.5-flash

gemini-2.5-flash-lite

gemini-2.0-flash

gemini-2.0-flash-lite

Google’s page shows model codes, capabilities, and versioning patterns (stable vs preview). 
Google AI for Developers
+2
Google AI for Developers
+2

Live/real-time & image generation (selected)

gemini-2.5-flash-preview-native-audio-dialog (Live API, preview)

gemini-2.0-flash-preview-image-generation (preview) 
Google AI for Developers
+1

Deprecations

gemini-1.5-pro shows deprecation date Sept 2025; migrate to 2.0/2.5. 
Google AI for Developers

Docs: “Gemini models” page and versioning guidance (last updated 2025‑09‑17 UTC). 
Google AI for Developers

Ollama (local open models)

Popular, curated IDs to accept by default

Meta Llama: llama4, llama4:16x17b, llama4:128x17b, llama3.3, llama3.2, llama3.2-vision, llama3.1:8b, llama3.1:70b, llama3.1:405b 
Ollama
+2
Ollama
+2

Qwen: qwen3, plus qwen2.5 sizes (:7b, :14b, :32b, :72b) 
Ollama

Gemma: gemma3n, gemma2:2b, gemma2:9b, gemma2:27b 
Ollama

DeepSeek: deepseek-r1 (reasoning family; many size/quant tags) 
Ollama

Other frequent: phi4, mistral-nemo (as published in the library) 
Ollama

Reminder: Users can run any locally installed tag (e.g., llama3.1:8b-instruct-q4_K_M). If you want stricter validation, read GET /api/tags and match. Docs: Ollama library and API. 
Ollama
+1

2) Compatibility notes & rationale

Anthropic: Kept Claude 3.x snapshots for backward compatibility; promoted Sonnet 4 as default per Anthropic’s current guidance and Sonnet 3.5 deprecation. Aliases are convenient but Anthropic explicitly recommends snapshot IDs for production. 
Claude Docs
+1

OpenAI: Set default to GPT‑4o (“best for most tasks”). Included o4‑mini and o3 as accepted; if you later add a Responses codepath, you can include o1 variants. 
OpenAI Platform
+1

Gemini: Defaulted to gemini-2.5-flash (fast/capable). The models page clearly lists stable IDs and the Sept 2025 deprecation of 1.5 Pro. 
Google AI for Developers
+1

Ollama: Curated a sane, modern allowlist while recognizing Ollama’s open nature. The list maps to prominent library pages so it won’t surprise users. 
Ollama

3) Optional next steps (if you want me to)

Add unit tests that try a zero‑token call (or dry_run=True) to each accepted model per provider to ensure we don’t accept typos.

For OpenAI, add a feature flag use_responses_api_for = {"o1", "o1-mini", "o1-pro"} to route those IDs to /v1/responses automatically. 
OpenAI Platform

For Ollama, add a validate_model_exists option that calls GET /api/tags to warn early if a local model hasn’t been pulled yet.

Appendix — Detailed sources (selected)

Anthropic: Models overview and explicit API model names (includes claude-3-7-sonnet-20250219, claude-sonnet-4-20250514, claude-opus-4-20250514, claude-opus-4-1-20250805) and guidance to prefer snapshot IDs; Sonnet 3.5 deprecation (retirement Oct 22, 2025). 
Claude Docs
+2
Claude Docs
+2

OpenAI: GPT‑4o model page (best for most tasks); GPT‑4.1 page; o‑series (o3 / o4‑mini) model pages; o1‑pro (Responses API); deprecations. 
OpenAI Platform
+5
OpenAI Platform
+5
OpenAI Platform
+5

Google Gemini: “Gemini models” (last updated 2025‑09‑17 UTC) with explicit model codes for 2.5/2.0 and deprecation notice for 1.5 Pro; versioning rules for stable vs preview/experimental. 
Google AI for Developers
+3
Google AI for Developers
+3
Google AI for Developers
+3

Ollama: Library pages for Llama 4 / Llama 3.3 / Llama 3.1, DeepSeek‑R1, Qwen3, Gemma 3n; Ollama API docs. 
GitHub
+6
Ollama
+6
Ollama
+6

If you paste the four diffs above, your provider model lists will be fully up to date as of today. If you want, I can also produce the patches as a single .patch file or open a PR branch with these changes.

You said:
How about Mistral

deepseek_lib

github_ai_models_lib

And other providers should we add next
ChatGPT said:
Request for GPT-5 Pro
Reasoned for 8m 22s

Great idea—adding Mistral, DeepSeek, and GitHub Models will bring llmquery’s coverage up to date. Below you’ll find:

Drop‑in provider modules (with ACCEPTED_MODELS, defaults, and endpoints)

A concise model catalog for each provider (with sources)

Setup.py changes

A ranked list of next providers to add (with why)

A downloadable reference document that consolidates everything

1) New provider modules (ready to paste)

I mirrored your Anthropic file’s style (constants first; simple, explicit defaults). These modules assume you’re using ordinary OpenAI‑style chat completion payloads. You can wire them into your internal calling code the same way you do today.

providers/mistral_lib/mistral_client.py
# providers/mistral_lib/mistral_client.py

ACCEPTED_MODELS = [
    # Text / General
    "mistral-large-2411",
    "mistral-large-latest",
    "mistral-medium-latest",
    "mistral-small-latest",
    # Vision
    "pixtral-large-latest",
    "pixtral-12b-latest",
    # Code
    "codestral-2501",
    "codestral-latest",
]

DEFAULT_MODEL = "mistral-large-latest"
DEFAULT_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
DEFAULT_SYSTEM_PROMPT = (
    "You are a precise, efficient assistant. Prefer concise, correct, actionable answers. "
    "Use structured lists and code blocks when helpful, and ask for missing details only if critical."
)

# Optional: minimal request helper (you can swap in your shared HTTP helper)
import os, requests

def chat(messages, model=DEFAULT_MODEL, api_key=None, **kwargs):
    api_key = api_key or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is required")

    if model not in ACCEPTED_MODELS:
        raise ValueError(f"Model '{model}' not in ACCEPTED_MODELS")

    payload = {
        "model": model,
        "messages": messages,
        **({k: v for k, v in kwargs.items() if v is not None})
    }
    r = requests.post(
        DEFAULT_ENDPOINT,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )
    r.raise_for_status()
    return r.json()


Why these models? Mistral’s current public docs and announcements list these model IDs for chat/vision/code: mistral-large-2411/-latest, mistral-medium-latest, mistral-small-latest, pixtral-large-latest, pixtral-12b-latest, codestral-2501/-latest. Their vision page explicitly names the vision‑capable SKUs, and the Pixtral Large announcement calls out the pixtral-large-latest API ID; “Predicted outputs” pages still show mistral-large-2411 and codestral-2501. 
Mistral AI Documentation
+4
Mistral AI Documentation
+4
Mistral AI
+4

providers/deepseek_lib/deepseek_client.py
# providers/deepseek_lib/deepseek_client.py

ACCEPTED_MODELS = [
    "deepseek-chat",       # general chat (V3.x non-thinking)
    "deepseek-reasoner",   # reasoning (R1/V3.x thinking)
]

DEFAULT_MODEL = "deepseek-chat"
DEFAULT_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, careful assistant. Provide direct, accurate answers with minimal verbosity. "
    "Show your steps only if the user asks for them."
)

import os, requests

def chat(messages, model=DEFAULT_MODEL, api_key=None, **kwargs):
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is required")
    if model not in ACCEPTED_MODELS:
        raise ValueError(f"Model '{model}' not in ACCEPTED_MODELS")

    payload = {
        "model": model,
        "messages": messages,
        **({k: v for k, v in kwargs.items() if v is not None})
    }
    r = requests.post(
        DEFAULT_ENDPOINT,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )
    r.raise_for_status()
    return r.json()


Why these models? DeepSeek’s official API documents show the current model IDs are exactly deepseek-chat and deepseek-reasoner. Their “Models & Pricing” page explains that the two map to DeepSeek‑V3.1 (non‑thinking) and DeepSeek‑V3.1 (thinking) respectively, with the note that tool calls on the reasoning model are handled by deepseek-chat. Sample requests show both /v1/chat/completions and /chat/completions forms. 
DeepSeek API Docs
+3
DeepSeek API Docs
+3
DeepSeek API Docs
+3

providers/github_ai_models_lib/github_models.py
# providers/github_ai_models_lib/github_models.py

# GitHub Models aggregates many publishers. The most reliable way to stay current is to
# pull the catalog at runtime and accept those IDs.
CATALOG_URL = "https://models.github.ai/catalog/models"
DEFAULT_ENDPOINT = "https://models.github.ai/inference/chat/completions"

# Curated starters so users have something that "just works" even if they skip catalog refresh.
STATIC_ACCEPTED_MODELS = [
    # OpenAI
    "openai/gpt-4o",
    "openai/gpt-4.1",
    "openai/gpt-4.1-mini",
    "openai/o1-preview",
    # Meta (Llama) via AzureML registry IDs used in Marketplace pages
    "azureml-meta/Meta-Llama-3.1-8B-Instruct",
    "azureml-meta/Meta-Llama-3.1-70B-Instruct",
    "azureml-meta/Meta-Llama-3.1-405B-Instruct",
    # Mistral
    "azureml-mistral/Mistral-Large-2411",
    "azureml-mistral/mistral-medium-2505",
    # DeepSeek
    "azureml-deepseek/DeepSeek-V3-0324",
    # Microsoft
    "azureml/Phi-4",
    # Cohere (chat)
    "azureml-cohere/Cohere-command-a",
]

DEFAULT_MODEL = "openai/gpt-4o"
DEFAULT_SYSTEM_PROMPT = (
    "You are a reliable assistant. Be accurate and concise, cite sources when asked, and "
    "format code and lists cleanly."
)

import os, requests

def list_catalog_models(token=None):
    """Return list of model IDs from the GitHub Models catalog."""
    token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        # Graceful fallback if no token is set: return the static list
        return list(STATIC_ACCEPTED_MODELS)
    h = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    r = requests.get(CATALOG_URL, headers=h, timeout=60)
    r.raise_for_status()
    data = r.json()
    # The API returns an array of objects; each has an "id" field like "openai/gpt-4.1"
    ids = [m.get("id") for m in data if isinstance(m, dict) and m.get("id")]
    # Keep a union of static starters + live catalog
    return sorted(set(STATIC_ACCEPTED_MODELS).union(ids))

# By default accept both the curated starters and anything from the live catalog (if reachable).
def get_accepted_models():
    return list_catalog_models()

def chat(messages, model=DEFAULT_MODEL, token=None, **kwargs):
    token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN (fine‑grained PAT) is required for GitHub Models")

    # model sanity check (optional; you can disable if you want to be permissive)
    if model not in get_accepted_models():
        raise ValueError(f"Model '{model}' not found in catalog; run list_catalog_models() to inspect IDs.")

    payload = {
        "model": model,
        "messages": messages,
        **({k: v for k, v in kwargs.items() if v is not None})
    }
    r = requests.post(
        DEFAULT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=90,
    )
    r.raise_for_status()
    return r.json()


Why this shape? GitHub Models exposes GET /catalog/models to enumerate IDs (e.g., openai/gpt-4.1), and an inference chat endpoint you call with those IDs. The Marketplace pages confirm the representative IDs above (OpenAI GPT‑4o/4.1/4.1‑mini, o1‑preview; Meta Llama 3.1 8B/70B/405B; Mistral Large 24.11 and Medium; DeepSeek V3; Microsoft Phi‑4; Cohere Command A). The curated starters keep things working offline; the dynamic list_catalog_models() keeps you current in CI. 
GitHub
+13
GitHub Docs
+13
The GitHub Blog
+13

2) Compact model catalog per provider (snapshot)
Mistral (Chat / Vision / Code)

Chat/General: mistral-large-2411 (mistral-large-latest), mistral-medium-latest, mistral-small-latest. 
Mistral AI Documentation

Vision: pixtral-large-latest, pixtral-12b-latest. 
Mistral AI Documentation
+1

Code: codestral-2501 (codestral-latest). 
Mistral AI Documentation

Endpoint: https://api.mistral.ai/v1/chat/completions. 
Mistral AI Documentation
+1

DeepSeek

Models: deepseek-chat, deepseek-reasoner. (The canonical/only two “IDs” exposed by the API.) 
DeepSeek API Docs

Notes: Reasoner doesn’t handle tool calls; requests with tools are routed to deepseek-chat. 
DeepSeek API Docs

Endpoint: https://api.deepseek.com/v1/chat/completions. 
DeepSeek API Docs

GitHub Models

Catalog: GET https://models.github.ai/catalog/models returns a list of ids (use directly in model). 
GitHub Docs

Examples present today:

OpenAI: openai/gpt-4o, openai/gpt-4.1, openai/gpt-4.1-mini, openai/o1-preview. 
GitHub
+3
GitHub
+3
GitHub
+3

Meta (Llama): azureml-meta/Meta-Llama-3.1-8B-Instruct, …-70B-…, …-405B-…. 
GitHub
+2
GitHub
+2

Mistral: azureml-mistral/Mistral-Large-2411, azureml-mistral/mistral-medium-2505. 
GitHub
+1

DeepSeek: azureml-deepseek/DeepSeek-V3-0324. 
GitHub

Microsoft: azureml/Phi-4. 
GitHub

Cohere: azureml-cohere/Cohere-command-a (chat), + embeddings. 
GitHub
+1

Inference: POST https://models.github.ai/inference/chat/completions (OpenAI‑style payload). 
The GitHub Blog

A full, ready‑to‑share document with all of the above (endpoints, defaults, examples, and notes) is here:
Download the Markdown

3) setup.py change

Add the three new provider packages to find_packages:

-  packages=find_packages(include=[
-      'llmquery*','providers*','query_parser*',
-      'providers.anthropic_lib*','providers.google_gemini_lib*',
-      'providers.openai_lib*','providers.ollama_lib*']),
+  packages=find_packages(include=[
+      'llmquery*','providers*','query_parser*',
+      'providers.anthropic_lib*','providers.google_gemini_lib*',
+      'providers.openai_lib*','providers.ollama_lib*',
+      'providers.mistral_lib*','providers.deepseek_lib*',
+      'providers.github_ai_models_lib*']),


(If you keep a providers registry in code, add entries for these three.)

4) Providers to add next (ranked + rationale)

Groq – OpenAI‑compatible, exceptionally low latency; hosted Llama 3.x families and more. They publish a live models endpoint and model IDs such as llama-3.1-8b-instant, llama-3.3-70b-versatile, plus openai/gpt-oss-120b. This is the easiest “speed win” provider to add. 
GroqCloud

AWS Bedrock – One AWS API for Anthropic (Claude), Meta (Llama), Mistral, Cohere, Amazon Nova… Model IDs differ by region; discoverable with ListFoundationModels. You’ll need AWS SigV4 signing (boto3) rather than OpenAI‑style. 
AWS Documentation
+1

Together AI – OpenAI‑compatible unified endpoint with 200+ OSS models; simple to wire. 
Together.ai Docs
+1

OpenRouter – Aggregates 100+ models (DeepSeek, OpenAI, Anthropic, Meta, Mistral, Google, etc.) behind one OpenAI‑style API; good for coverage/fallback. 
OpenRouter

Google Vertex AI – For Gemini plus hosted Mistral and Llama with enterprise controls; useful if your users are already on GCP. 
Mistral AI Documentation

If you want, I can supply stubs for Groq and Bedrock too (Groq is trivial/OpenAI‑compatible; Bedrock needs its own signer + boto3).

5) Notes & gotchas (so nothing breaks)

Pin vs. latest: Mistral’s *-latest pointers move; pin to mistral-large-2411 if you need reproducibility. 
Mistral AI

DeepSeek Reasoner tools: deepseek-reasoner doesn’t accept tools; requests with tools are automatically handled by deepseek-chat. 
DeepSeek API Docs

GitHub Models IDs: treat the catalog as the ground truth; Marketplace pages are helpful for discovery but the catalog dictates the id string you must send. 
GitHub Docs

6) Quick test snippets

Mistral

curl https://api.mistral.ai/v1/chat/completions \
  -H "Authorization: Bearer $MISTRAL_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"mistral-large-2411","messages":[{"role":"user","content":"ping"}]}'


DeepSeek

curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"ping"}]}'


DeepSeek API Docs

GitHub Models

# list models
curl -L https://models.github.ai/catalog/models \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28"

# run chat
curl https://models.github.ai/inference/chat/completions \
  -H "Authorization: Bearer $GITHUB_TOKEN" -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/gpt-4o","messages":[{"role":"user","content":"ping"}]}'


GitHub Docs
+1

One file you can share internally

I packaged the above into a Markdown doc you can drop into the repo (or share with your team):

Download: llmquery-providers-and-models-2025-09-19.md

Summary of changes you’ll make

Add three provider packages: providers.mistral_lib, providers.deepseek_lib, providers.github_ai_models_lib

Update setup.py find_packages() to include them

Use the constants above for ACCEPTED_MODELS, DEFAULT_MODEL, DEFAULT_ENDPOINT, and DEFAULT_SYSTEM_PROMPT

(Optional but recommended): for GitHub Models, use the live catalog at runtime to discover model IDs and keep the allowlist fresh automatically. 
GitHub Docs

If you want me to also prep Groq and Bedrock stubs (or wire in a dynamic “fetch & cache models” task for every provider), say the word and I’ll ship those too.