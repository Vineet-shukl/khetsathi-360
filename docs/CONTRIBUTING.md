# Contributing to KhetSathi 360

Welcome to **KhetSathi 360**. We maintain a high code quality standard ("Plankton Quality Gate") ensuring deterministic agronomic safety, zero regressions, and full reproducibility.

---

## 1. Development Prerequisites

- **Python 3.11+** (FastAPI, Pydantic v2, LightGBM, scikit-learn, httpx)
- **Node.js 20+** (for the optional `client/` React 19 dashboard)
- **Git**

---

## 2. Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Vineet-shukl/khetsathi-360.git
cd khetsathi-360

# Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# (Optional) Setup React enterprise client
cd client && npm install && cd ..
```

---

## 3. Available Commands & Scripts

<!-- AUTO-GENERATED FROM repository tooling -->
| Command | Category | Description |
|:--------|:--------:|:------------|
| `python scripts/quality_gate.py` | Quality Gate | Enforces formatting, linting, and runs all 48 test suites with promotion gates. |
| `python -m unittest discover -s tests -v` | Testing | Executes all backend and API contract tests. |
| `python ml_pipeline/train.py` | Machine Learning | Retrains the 695-district spatial IDW bundle and LightGBM residual model. |
| `python ml_pipeline/evaluate.py` | Model Validation | Evaluates temporal holdout promotion gates (MAE, latency, safety envelope). |
| `uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload` | Local Server | Starts FastAPI server with live reload at `http://localhost:8000`. |
| `cd client && npm run build` | Frontend Build | Compiles React 19 client and deploys assets safely to `frontend/index_react.html`. |
| `python -m ruff format app tests ml_pipeline` | Code Style | Auto-formats Python code using Ruff. |
| `python -m ruff check --fix app tests ml_pipeline` | Code Style | Runs fast static linting and automated fixes. |
<!-- /AUTO-GENERATED -->

---

## 4. The 3-Phase Plankton Quality Gate

Before any commit or pull request, you **must** pass the quality gate:

```bash
python scripts/quality_gate.py
```

The gate rigorously validates:
1. **Phase 1: Code Formatting**: Verifies PEP 8 formatting with `ruff format --check`.
2. **Phase 2: Static Analysis**: Detects unused imports, type ambiguities, and lint issues with `ruff check`.
3. **Phase 3: Unit Tests & Promotion Gates**:
   - Executes all 48 test suites across API contracts, geospatial lookups, and OCR guardrails.
   - Evaluates ML temporal holdout partition (years > 2015): requires $\ge 25\%$ MAE improvement over naive baseline and $p95$ latency $\le 50\text{ ms}$.

---

## 5. Architectural Decision Guidelines

If introducing structural architectural changes (e.g., changes to storage, API protocols, caching, or ML inference):
1. Propose an ADR following the template in [docs/adr/template.md](adr/template.md).
2. Number the ADR sequentially and record the rationale, rejected alternatives, and consequences.
3. Update [docs/adr/README.md](adr/README.md).
