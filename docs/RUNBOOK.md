# Operational Runbook: KhetSathi 360

This runbook guides production deployment, monitoring, health verification, and incident mitigation for **KhetSathi 360**.

---

## 1. Production Architecture Overview

- **Host**: Render Cloud Web Service (`render.yaml`)
- **Region**: Singapore (`singapore`)
- **Runtime**: Python 3.11.9
- **Command**: `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
- **Primary Live URL**: [https://khetsathi-360.onrender.com/](https://khetsathi-360.onrender.com/)

---

## 2. Health Check & Live Monitoring Endpoints

<!-- AUTO-GENERATED FROM app/api.py -->
| Endpoint | Method | Expected Output | Purpose |
|:---------|:------:|:----------------|:--------|
| `/api/v1/health` | `GET` | `{"status": "healthy", "ml_residual": true, ...}` | Primary liveness & model promotion gate check. |
| `/api/v1/district/baseline?lat=25.5928&lon=83.577` | `GET` | HTTP 200 with Ghazipur soil baselines | Geospatial IDW engine health. |
| `/api/v1/weather?lat=25.5928&lon=83.577&lang=hi` | `GET` | HTTP 200 with forecast and FAO-56 ET0 | Weather adapter upstream connectivity. |
| `/sw.js` | `GET` | HTTP 200 (`Cache-Control: no-cache`) | PWA service worker script delivery. |
<!-- /AUTO-GENERATED -->

```bash
# Verify health via curl:
curl -s https://khetsathi-360.onrender.com/api/v1/health | jq .
```

---

## 3. Deployment Procedure

Deployments to Render are automatically triggered on Git pushes to `main`:

```bash
# 1. Run local Plankton Quality Gate
python scripts/quality_gate.py

# 2. Push to GitHub main branch
git push origin main

# 3. Observe deployment logs on Render dashboard or poll /api/v1/health
```

---

## 4. PWA Service Worker Cache Eviction Protocol

If a client browser caches an older release:
- Service Worker versioning is maintained in `frontend/sw.js` (`const CACHE_NAME = 'khetsathi-v2.2'`).
- The Service Worker enforces **Network-First** for navigation requests (`mode === 'navigate'`).
- Bumping the `CACHE_NAME` constant automatically evicts all prior cache keys during the `activate` event (`caches.delete(key)`).
- Farmers can also perform a hard reload (`Ctrl + F5` or clearing site data via Chrome settings).

---

## 5. Rollback Procedures

If a deployment introduces regressions:
1. Identify the last known good commit SHA via `git log --oneline -n 5`.
2. Revert the commit or push the stable commit to `main`:
   ```bash
   git revert <bad-commit-sha>
   python scripts/quality_gate.py
   git push origin main
   ```
3. Verify `/api/v1/health` status turns green within 90 seconds.
