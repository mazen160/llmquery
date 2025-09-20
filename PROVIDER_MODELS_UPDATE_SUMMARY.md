# LLMQuery Provider Models Update Summary
**Date**: September 20, 2025  
**Updated by**: AI Assistant based on research from PROMPT.md

## Overview
This document summarizes all the updates made to the LLMQuery project's provider models based on the comprehensive research provided in PROMPT.md. The updates bring all provider models up to date as of September 2025.

## Updated Existing Providers

### 1. Anthropic Claude (`providers/anthropic_lib/anthropic_claude.py`)

**Previous Models:**
- claude-3-5-sonnet-20241022, claude-3-5-sonnet-latest
- claude-3-5-haiku-20241022, claude-3-5-haiku-latest  
- claude-3-opus-20240229, claude-3-opus-latest
- claude-3-sonnet-20240229, claude-3-haiku-20240307

**Updated Models:**
- **Claude 4.x (NEW):**
  - `claude-opus-4-1-20250805` (newest Opus snapshot)
  - `claude-opus-4-20250514` (Opus 4)
  - `claude-sonnet-4-20250514` (Sonnet 4)
- **Claude 3.7 (NEW):**
  - `claude-3-7-sonnet-20250219`
  - `claude-3-7-sonnet-latest`
- **Claude 3.5/3 (kept for compatibility):**
  - All previous models maintained
  - Note: Sonnet 3.5 deprecated Oct 22, 2025

**Default Model Changed:** `claude-3-5-haiku-latest` → `claude-sonnet-4-20250514`

### 2. OpenAI (`providers/openai_lib/openai.py`)

**Key New Models Added:**
- **Current Recommended:**
  - `gpt-4.1`, `gpt-4.1-mini` (NEW)
- **Reasoning Models:**
  - `o4-mini`, `o3` (NEW)

**Default Model Changed:** `gpt-4o-mini` → `gpt-4o` (best for most tasks per OpenAI docs)

**Note:** All existing models maintained for backward compatibility.

### 3. Google Gemini (`providers/google_gemini_lib/google_gemini.py`)

**Previous Models:**
- gemini-1.5-flash, gemini-2.0-flash-exp, gemini-1.5-pro

**Updated Models:**
- **Gemini 2.5 (NEW - top tier):**
  - `gemini-2.5-pro`
  - `gemini-2.5-flash`
  - `gemini-2.5-flash-lite`
- **Gemini 2.0 (NEW):**
  - `gemini-2.0-flash`
  - `gemini-2.0-flash-lite`
- **1.5 (compatibility):**
  - All previous models maintained
  - Note: 1.5 Pro deprecates Sept 2025

**Default Model Changed:** `gemini-1.5-flash` → `gemini-2.5-flash`

### 4. Ollama (`providers/ollama_lib/ollama.py`)

**Major Addition:** Added comprehensive `ACCEPTED_MODELS` list (previously had none)

**New Models Added:**
- **Meta Llama:** llama4, llama4:16x17b, llama4:128x17b, llama3.3, llama3.2, llama3.2-vision, llama3.1 variants
- **Alibaba Qwen:** qwen3, qwen2.5 variants (7b, 14b, 32b, 72b)
- **Google Gemma:** gemma3n, gemma2 variants (2b, 9b, 27b)
- **DeepSeek:** deepseek-r1
- **Others:** phi4, mistral-nemo

**Default Model:** Remains `llama3.3`

## New Providers Added

### 5. Mistral (`providers/mistral_lib/mistral.py`) - **NEW**

**Models:**
- **Text/General:** mistral-large-2411, mistral-large-latest, mistral-medium-latest, mistral-small-latest
- **Vision:** pixtral-large-latest, pixtral-12b-latest
- **Code:** codestral-2501, codestral-latest

**Default Model:** `mistral-large-latest`  
**Endpoint:** `https://api.mistral.ai/v1/chat/completions`  
**API Key:** `MISTRAL_API_KEY`

### 6. DeepSeek (`providers/deepseek_lib/deepseek.py`) - **NEW**

**Models:**
- `deepseek-chat` (general chat, V3.x non-thinking)
- `deepseek-reasoner` (reasoning, R1/V3.x thinking)

**Default Model:** `deepseek-chat`  
**Endpoint:** `https://api.deepseek.com/v1/chat/completions`  
**API Key:** `DEEPSEEK_API_KEY`

**Note:** Reasoner model doesn't handle tool calls; requests with tools are routed to deepseek-chat.

### 7. GitHub AI Models (`providers/github_ai_models_lib/github_ai_models.py`) - **NEW**

**Dynamic Model Discovery:** Fetches available models from GitHub's catalog API at runtime.

**Static Fallback Models:**
- **OpenAI:** openai/gpt-4o, openai/gpt-4.1, openai/gpt-4.1-mini, openai/o1-preview
- **Meta Llama:** azureml-meta/Meta-Llama-3.1-8B/70B/405B-Instruct
- **Mistral:** azureml-mistral/Mistral-Large-2411, azureml-mistral/mistral-medium-2505
- **DeepSeek:** azureml-deepseek/DeepSeek-V3-0324
- **Microsoft:** azureml/Phi-4
- **Cohere:** azureml-cohere/Cohere-command-a

**Default Model:** `openai/gpt-4o`  
**Endpoint:** `https://models.github.ai/inference/chat/completions`  
**API Key:** `GITHUB_TOKEN` or `GH_TOKEN`

**Special Feature:** `list_catalog_models()` function dynamically fetches current available models.

## Setup.py Status
✅ **Already Updated** - The setup.py file already included all the new provider packages in the `find_packages()` configuration.

## API Key Requirements

### New Environment Variables Needed:
- `MISTRAL_API_KEY` - For Mistral provider
- `DEEPSEEK_API_KEY` - For DeepSeek provider  
- `GITHUB_TOKEN` or `GH_TOKEN` - For GitHub AI Models provider (fine-grained PAT required)

### Existing Environment Variables (unchanged):
- `ANTHROPIC_API_KEY` - For Anthropic Claude
- `OPENAI_API_KEY` - For OpenAI
- `GOOGLE_GEMINI_API_KEY` - For Google Gemini
- (No API key needed for Ollama - local installation)

## Deprecation Warnings

1. **Anthropic:** Claude 3.5 Sonnet (claude-3-5-sonnet-20241022) deprecated, retirement Oct 22, 2025
2. **Google:** Gemini 1.5 Pro shows deprecation date Sept 2025; migrate to 2.0/2.5
3. **OpenAI:** GPT-4 legacy models retired from ChatGPT, various stages of deprecation

## Recommendations for Users

1. **Migrate to newer models** for better performance:
   - Anthropic: Use Claude 4.x models
   - OpenAI: Use GPT-4o or GPT-4.1 series
   - Google: Use Gemini 2.5 series

2. **Test new providers** for cost/performance benefits:
   - DeepSeek offers competitive reasoning capabilities
   - Mistral provides strong European-based alternative
   - GitHub Models offers unified access to multiple providers

3. **Update API keys** in environment variables for new providers

## File Changes Made

### Modified Files:
1. `providers/anthropic_lib/anthropic_claude.py` - Updated models and default
2. `providers/openai_lib/openai.py` - Added new models and updated default  
3. `providers/google_gemini_lib/google_gemini.py` - Added 2.5/2.0 series
4. `providers/ollama_lib/ollama.py` - Added comprehensive model list

### New Files Created:
1. `providers/mistral_lib/mistral.py` - Complete Mistral provider
2. `providers/mistral_lib/__init__.py` - Module initialization
3. `providers/deepseek_lib/deepseek.py` - Complete DeepSeek provider
4. `providers/deepseek_lib/__init__.py` - Module initialization
5. `providers/github_ai_models_lib/github_ai_models.py` - Complete GitHub Models provider
6. `providers/github_ai_models_lib/__init__.py` - Module initialization

## Testing Recommendations

Before deploying these changes:

1. **Test API connectivity** for each provider with a simple query
2. **Verify API keys** are properly configured in environment
3. **Test model validation** to ensure accepted models work correctly
4. **Check backward compatibility** with existing templates and queries

## Next Steps Suggested

1. **Add unit tests** for new providers
2. **Update documentation** to reflect new models and providers
3. **Consider adding Groq and AWS Bedrock** providers (mentioned in research)
4. **Update example templates** to showcase new provider capabilities

---
*This update brings LLMQuery up to date with the latest models available as of September 2025, significantly expanding the platform's capabilities and provider coverage.*
