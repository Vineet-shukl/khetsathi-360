# Environment Variable Reference

This document catalogs all environment variables recognized by **KhetSathi 360**.

<!-- AUTO-GENERATED FROM .env.example -->
| Variable | Required | Default | Type | Description |
|:---------|:--------:|:-------:|:----:|:------------|
| `PORT` | No | `8000` | Integer | HTTP port on which the FastAPI application listens. Automatically set by Render. |
| `HOST` | No | `0.0.0.0` | String | Network interface binding. |
| `ENABLE_ML_RESIDUAL` | No | `true` | Boolean string (`true`/`false`) | Enables Tier-2 LightGBM bounded ML residual calculations alongside deterministic ICAR base. |
| `GEMINI_API_KEY` | No | `""` | String | API key for Google Gemini 1.5 Flash Multimodal Vision OCR. If absent, fallback baseline applies. |
| `PYTHON_VERSION` | No | `3.11.9` | String | Target Python runtime version for containerized and Render deployments. |
<!-- /AUTO-GENERATED -->

## Production Notes
- **Zero-Cost Operation**: The core advisory engine, spatial IDW model, and weather integrations function **without any external paid API keys**.
- **Gemini Key Setup**: To enable live smartphone camera scanning of Soil Health Cards, obtain a key from [Google AI Studio](https://aistudio.google.com/) and export it in your shell or Render environment dashboard.
