---
title: KhetSathi 360 - National Agri Decision Platform
emoji: 🌾
colorFrom: green
colorTo: emerald
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# KhetSathi 360 — Pan-India Hybrid Agronomy Platform

Complete unified repository combining documentation, reference tables, real 695-district Soil Health Card data, hybrid ML + FastAPI backend, and bilingual Farmer/Investor frontend.

## Structure
- `app/` — FastAPI service (`api.py`), Pydantic contracts (`contracts.py`), deterministic ICAR/FAO-56 engine (`baseline_engine.py`), bounded residual ML (`ml_residual.py`), and 695-district spatial soil model (`district_soil_model.py`).
- `ml_pipeline/` — Reproducible training (`train.py`) and automated promotion gates (`evaluate.py`).
- `data/` — `CropDataset-Enhanced.csv` (695 Indian districts), `reference/` tables, and `raw/` (drop large local datasets here; gitignored).
- `frontend/index.html` — Self-contained bilingual UI with **🌾 किसान सलाहकार (Kisan Mitra)** and **🧪 मिट्टी परीक्षण व FPO केंद्र**.
- `frontend/portal.html` — Enterprise Operations & Partner Intelligence Portal.
- `docs/` & `plans/` — PRD, Architecture, API Catalog, Field Research Protocol, and 10-step Build Plan.
- `tests/` — Unit and FastAPI integration test suite.

## Quickstart
```bash
pip install -r requirements.txt
python3 ml_pipeline/train.py
python3 ml_pipeline/evaluate.py
python3 -m unittest discover -s tests -v
uvicorn app.api:app --host 0.0.0.0 --port 7860 --reload
```
