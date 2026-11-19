# KhetSathi 360 — Zero-Cost Deployment Guide for Investors & Mentors

> **Goal**: Deploy KhetSathi 360 to a permanent, public HTTPS link that runs 24/7 with **zero hosting cost**, so you can share it with investors, mentors (1M1B), and farmers.

---

## 🎯 What URLs Will Be Live After Deployment?

Once deployed, your live domain (e.g., `https://khetsathi-360.onrender.com`) will provide all 4 interactive surfaces:

| Surface | Path | Purpose |
| :--- | :--- | :--- |
| **💼 Investor Pitch Showcase** | `/investor` | Dark-themed executive pitch dashboard with live ROI simulation, coverage analytics, and traction metrics. |
| **🌾 Farmer Advisory PWA** | `/` or `/ui` | High-contrast, bilingual (Hindi/English) voice-enabled agronomy PWA with GPS geolocation. |
| **📊 FPO / Soil Health Scanner** | `/static/fpo_dashboard.html` | Extension agent portal with 12-parameter Soil Health Card OCR classification and village analytics. |
| **⚡ Interactive API Docs** | `/docs` | OpenAPI / Swagger interactive documentation with live test payloads. |

---

## 🚀 Method 1: Render.com (Recommended — 3 Minutes, 100% Free)

Render provides **750 free instance hours every month** (enough to run 1 web service 24/7 for free). It requires **no credit card**.

### Step 1: Initialize Git & Push to GitHub
Open PowerShell in `x:\khetsathi-360\` and run:

```powershell
# 1. Initialize git if not already done
git init
git add .
git commit -m "feat: investor-ready KhetSathi 360 platform"

# 2. Link to your GitHub account (create a new public repo named 'khetsathi-360' on github.com first)
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/khetsathi-360.git
git push -u origin main
```
*(Note: `data/raw/` is already in `.gitignore`, so only lean code and pre-trained model bundles will be pushed in seconds.)*

### Step 2: Deploy on Render
1. Go to **[render.com](https://render.com)** and sign up / log in with your GitHub account.
2. Click **New +** > **Web Service**.
3. Select your `khetsathi-360` repository.
4. Render will automatically read the included `render.yaml`! If filling manually:
   - **Name**: `khetsathi-360`
   - **Environment**: `Python 3`
   - **Region**: `Singapore` or `Oregon`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` ($0/month)
5. Click **Create Web Service**.

Render will build and deploy the app in under 2 minutes. Your live link will be:
👉 **`https://khetsathi-360.onrender.com/investor`**

---

## ⚡ Method 2: Hugging Face Spaces (Best for ML & Zero Sleep, 100% Free)

Hugging Face Spaces provides **2 vCPUs and 16 GB RAM completely free forever**. It never shuts down and has generous bandwidth.

1. Go to **[huggingface.co/new-space](https://huggingface.co/new-space)**.
2. Enter Space Name: `khetsathi-360`.
3. Select **Docker** as the Space SDK (Blank).
4. Set Space hardware to **Free CPU (2 vCPU · 16 GB RAM)**.
5. In your local terminal, push to your Hugging Face space:
   ```powershell
   git remote add space https://huggingface.co/spaces/<YOUR_HF_USERNAME>/khetsathi-360
   git push space main
   ```
6. Hugging Face will automatically build the `Dockerfile` and give you a permanent link:
   👉 **`https://<YOUR_HF_USERNAME>-khetsathi-360.hf.space/investor`**

---

## ⚡ Method 3: Instant Live Link Right Now (30 Seconds — For Urgent Demos)

If an investor is on a call or WhatsApp right now and you need an instant public HTTPS link from your laptop without pushing to GitHub first:

1. **Start the local server** in one PowerShell window:
   ```powershell
   python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
   ```

2. **Open a second PowerShell window** and create a free instant tunnel:
   ```powershell
   # Using npx (Node.js is already installed on your PC):
   npx localtunnel --port 8000 --subdomain khetsathi360
   ```
   *OR using SSH (built into Windows):*
   ```powershell
   ssh -R 80:localhost:8000 a.pinggy.io
   ```

3. It will output a public HTTPS URL (like `https://khetsathi360.loca.lt/investor` or `https://xxxx.a.pinggy.link/investor`) that anyone anywhere in the world can open on their phone immediately!

---

## 📊 Summary of What the Investor Sees

```
                           KHETSATHI 360 CLOUD DEPLOYMENT
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
         INVESTOR SHOWCASE                              FARMER ADVISORY PWA
     (/investor)                                     (/ or /ui)
  - 695 Districts Coverage                       - Real-time GPS Geolocation
  - 10.8M+ Soil Test Observations                - Open-Meteo Live NWP Weather
  - 59.6% MAE Model Improvement                  - ICAR/FAO-56 Irrigation Engine
  - Interactive ROI & MSP Simulator              - Bilingual Voice Speech Readout
  - UN SDG 2, 12, 13 Alignment                   - WCAG 2.2 AA Accessibility
```
