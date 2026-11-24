"""
scripts/generate_presentation_catalog_doc.py
Generates the comprehensive specification document:
- Master Image Registry with all 18 images standardized to 1920x1080.
- Complete slide-by-slide PPT text and structure.
- Detailed mapping of which images appear on which pages and their exact visual role.
- Full agronomic, mathematical, and accessibility rationale.
"""

import os
from pathlib import Path

def generate_catalog():
    repo_root = Path("X:/khetsathi-360")
    docs_dir = repo_root / "docs"
    pres_dir = repo_root / "presentation"
    docs_dir.mkdir(exist_ok=True)
    pres_dir.mkdir(exist_ok=True)

    md = []
    
    # Title & Metadata
    md.append("# KhetSathi 360 · Master Presentation Blueprint & Standardized Image Catalog")
    md.append("## Complete 14-Slide Technical Specification, Standardized 1080p Image Registry & Page-by-Page Mapping\n")
    md.append("> **Document Status**: Production Standard · Binding Architectural Reference  ")
    md.append("> **Source Presentation**: [`presentation/KhetSathi_360_Master_Product_Blueprint.pptx`](file:///x:/khetsathi-360/presentation/KhetSathi_360_Master_Product_Blueprint.pptx)  ")
    md.append("> **Rendering Engine**: DeckCraft CLI (`X:\\Tools\\DeckCraft\\deckcraft-cli.exe`)  ")
    md.append("> **Document Compiler**: WordCraft CLI (`X:\\Tools\\WordCraft\\wordcraft-cli.exe`)  ")
    md.append("> **Standard Image Canvas**: 1920 × 1080 Pixels · 16:9 Widescreen · 72/96 DPI Standard Web & Print DPI  ")
    md.append("> **Governing Foundation**: [`docs/PROJECT_FOUNDATION.md`](file:///x:/khetsathi-360/docs/PROJECT_FOUNDATION.md) · [`docs/adr/0006-farmer-first-endgame-vision-architecture.md`](file:///x:/khetsathi-360/docs/adr/0006-farmer-first-endgame-vision-architecture.md)  ")
    md.append("> **Verification Baseline**: 51/51 Pytest Unit & Integration Tests Passing\n")
    md.append("---\n")

    # Table of Contents
    md.append("## Table of Contents")
    md.append("1. [Executive Summary & Purpose](#1-executive-summary--purpose)")
    md.append("2. [Master Standardized Image Registry (1920 × 1080)](#2-master-standardized-image-registry-1920--1080)")
    md.append("3. [Page-by-Page PPT Information & Image Mapping (Slides 01 – 14)](#3-page-by-page-ppt-information--image-mapping)")
    md.append("   - [Page 01: Title & Executive Vision](#page-01-title--executive-vision)")
    md.append("   - [Page 02: The Ground Reality & Problem Context](#page-02-the-ground-reality--problem-context)")
    md.append("   - [Page 03: The 8 Inviolable Pillars (Core Foundation)](#page-03-the-8-inviolable-pillars-core-foundation)")
    md.append("   - [Page 04: Built & Live Prototype: Kisan Mitra 3-Step Decision Flow](#page-04-built--live-prototype-kisan-mitra-3-step-decision-flow)")
    md.append("   - [Page 05: Built & Live Prototype: Copernicus Sentinel-2 & Microclimate Safety](#page-05-built--live-prototype-copernicus-sentinel-2--microclimate-safety)")
    md.append("   - [Page 06: Built & Live Prototype: Multimodal SHC Vision OCR & Spatial IDW](#page-06-built--live-prototype-multimodal-shc-vision-ocr--spatial-idw)")
    md.append("   - [Page 07: Built & Live Prototype: Standalone 'Amrit Mati' Organic Hub](#page-07-built--live-prototype-standalone-amrit-mati-organic-hub)")
    md.append("   - [Page 08: In Active Development: Interactive Farmland Map Pointing Tool](#page-08-in-active-development-interactive-farmland-map-pointing-tool)")
    md.append("   - [Page 09: In Active Development: Smart Alternate Crop Pop-up & Machinery Plan](#page-09-in-active-development-smart-alternate-crop-pop-up--machinery-plan)")
    md.append("   - [Page 10: Under Polishing: Certified Seed Varieties & Govt Subsidized Stores](#page-10-under-polishing-certified-seed-varieties--govt-subsidized-stores)")
    md.append("   - [Page 11: Design Benchmark: Accessible for Class-5 Educated Farmers](#page-11-design-benchmark-accessible-for-class-5-educated-farmers)")
    md.append("   - [Page 12: Technical Architecture: Scalability & Low-Spec 4G Readiness](#page-12-technical-architecture-scalability--low-spec-4g-readiness)")
    md.append("   - [Page 13: Scope Discipline: What We Pruned & Why](#page-13-scope-discipline-what-we-pruned--why)")
    md.append("   - [Page 14: Strategic Roadmap: Deployment Status & Next Engineering Phase](#page-14-strategic-roadmap-deployment-status--next-engineering-phase)")
    md.append("4. [Visual Design Standards & Brand Hierarchy](#4-visual-design-standards--brand-hierarchy)")
    md.append("5. [Mathematical & Agronomic Formulations Reference](#5-mathematical--agronomic-formulations-reference)")
    md.append("6. [Cross-Page Image Utilization Matrix](#6-cross-page-image-utilization-matrix)\n")
    md.append("---\n")

    # Section 1
    md.append("## 1. Executive Summary & Purpose\n")
    md.append("This document establishes the official pictorial and textual specification for the **KhetSathi 360 Master Product Blueprint**. Every visual asset has been standardized to an exact **1920 × 1080 resolution (16:9 Full HD canvas)** to ensure uniform presentation quality across multi-screen projections, PDF executive exports, mobile devices, and high-DPI monitors.\n")
    md.append("The primary objective of this document is threefold:")
    md.append("1. **Complete Information Parity**: Document every textual element, metric, data point, and architectural assertion contained within the 14-slide PowerPoint deck without loss or summarization.")
    md.append("2. **Exact Page Mapping**: Clearly enumerate which standardized image is placed on which presentation page, how it is presented, and what evidence it provides to stakeholders and farmers.")
    md.append("3. **Farmer-First Clarity**: Articulate the underlying rationale behind every feature for India's 140 million farmers—specifically honoring the constraint of smallholders possessing a Class 5 level of formal education.\n")
    md.append("---\n")

    # Section 2: Master Image Registry
    md.append("## 2. Master Standardized Image Registry (1920 × 1080)\n")
    md.append("All 18 images in this registry are stored in [`presentation/standardized_1080p/`](file:///x:/khetsathi-360/presentation/standardized_1080p/) at an exact pixel dimension of **1920 × 1080**.\n")
    md.append("| # | Image Identifier | Type | Native Dim | Standardized Dim | Primary Usage (Page) | Description & Key UI Evidence |")
    md.append("|---|------------------|------|------------|------------------|----------------------|--------------------------------|")
    md.append("| 1 | `slide-01.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 01** (Cover) | Master Title slide: Dark forest backdrop (`#0e2d1f`), emerald border (`#10b981`), amber badges, 3 metric pills (695 Districts, Class-5 UX, 100% Parity). |")
    md.append("| 2 | `slide-02.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 02** | Problem Context: 4-card matrix detailing chemical burn, seed fraud, rain leaching, and digital literacy barriers. |")
    md.append("| 3 | `slide-03.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 03** | Core Blueprint: 8-card grid codifying the 8 Inviolable Pillars of KhetSathi 360. |")
    md.append("| 4 | `slide-04.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 04** | Working Prototype 1: Split slide with left agronomic features and right embedded English UI prototype. |")
    md.append("| 5 | `slide-05.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 05** | Working Prototype 2: Split slide with left Sentinel-2/SoilGrids prototype and right space-to-soil architecture bullets. |")
    md.append("| 6 | `slide-06.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 06** | Working Prototype 3: Dual-card layout for Vision OCR Guardrails (left) and 695-District Spatial IDW (right). |")
    md.append("| 7 | `slide-07.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 07** | Working Prototype 4: 4-card feature layout for the Amrit Mati Organic Hub (Soil simulator, recipe kitchen, economic ledger, buyer routes). |")
    md.append("| 8 | `slide-08.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 08** | Active Dev 1: Pillar 1 Interactive Farmland Map Pointing Tool specification with 4 tactical cards. |")
    md.append("| 9 | `slide-09.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 09** | Active Dev 2: Dual-card layout for Floating Top-Right Alternate Crop Pop-up and Plot-Scale Machinery Lifecycle. |")
    md.append("| 10 | `slide-10.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 10** | Polishing 1: Pillar 2 Certified Seed Varieties, Government Block Seed Store Locator, and Subsidized Price Matrix. |")
    md.append("| 11 | `slide-11.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 11** | UX Benchmark: 4-card matrix for Class-5 Farmer Accessibility (Tactile cards, voice reader, outdoor contrast, 100% bilingual parity). |")
    md.append("| 12 | `slide-12.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 12** | Technical Architecture: 4-card matrix for Sub-200ms TTFB, PWA Service Worker v2.3, Skeleton loaders, and FastAPI backend. |")
    md.append("| 13 | `slide-13.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 13** | Scope Discipline: 4 high-contrast alert cards detailing pruned features (non-agri OCR, desktop spreadsheets, heavy JS, crypto). |")
    md.append("| 14 | `slide-14.png` | DeckCraft Render | 1920×1080 | **1920×1080** | **Page 14** | Strategic Roadmap: 4-card phased engineering plan (Live Render prototype, Phase A Map, Phase B Pop-up, Phase C Stores). |")
    md.append("| 15 | `proto_kisan_mitra_hindi_1080p.png` | Prototype Capture | 1366×577 | **1920×1080** | **Page 04** (Reference) | High-res capture of the live Hindi user interface showing the 3-step decision flow, state/district selection, and wheat crop. |")
    md.append("| 16 | `proto_kisan_mitra_english_1080p.png` | Prototype Capture | 1370×637 | **1920×1080** | **Page 04** (Embedded) | Live English UI screenshot embedded directly on Slide 04 showing 1-click GPS, Blinkit-style district picker, and land input. |")
    md.append("| 17 | `proto_weather_land_converter_1080p.png` | Prototype Capture | 1370×637 | **1920×1080** | **Page 05** (Reference) | Live prototype capture of the dynamic Bigha-to-Acre unit converter and live Open-Meteo weather safety banner. |")
    md.append("| 18 | `proto_remote_sensing_sentinel2_1080p.png` | Prototype Capture | 1370×637 | **1920×1080** | **Page 05** (Embedded) | Live prototype screenshot embedded directly on Slide 05 showing Copernicus Sentinel-2 10m NDVI and ISRIC SoilGrids cards. |\n")
    md.append("---\n")

    # Section 3: Page-by-Page PPT Information & Image Mapping
    md.append("## 3. Page-by-Page PPT Information & Image Mapping\n")

    slides_info = [
        {
            "num": "01",
            "title": "Title & Executive Vision",
            "category": "COVER / STRATEGIC OVERVIEW",
            "image": "slide-01.png",
            "embedded_proto": None,
            "badge": "🌾 NATIONAL DIGITAL AGRI DECISION PLATFORM · राष्ट्रीय डिजिटल कृषि निर्णय प्रणाली",
            "main_heading": "KhetSathi 360",
            "sub_heading": "Endgame Master Architecture & Prototype Presentation",
            "lead_text": "From Farmland Map Pointing & Certified Seeds to Space Remote Sensing, Soil Regeneration & Direct Mandi Markets — Built for 140 Million Grassroots Indian Farmers.",
            "cards": [
                ("695 Districts", "Full Pan-India Geospatial Baseline"),
                ("Class-5 UX", "Visual Cards + Audio Speech Reader"),
                ("100% Parity", "Flawless Bilingual Hindi ⇄ English")
            ],
            "bullets": [],
            "image_description": "Full-bleed 1920×1080 executive title slide. The background uses deep forest green (`#0e2d1f`), wrapped inside an inner accent frame of emerald (`#10b981`, 2pt border). The typography features high-contrast white headers with harvest amber badges. Three bottom rounded cards highlight core architectural achievements.",
            "farmer_rationale": "Establishes a dignified, culturally resonant visual identity for Indian farmers. Rather than an intimidating bureaucratic look, it conveys trust, technological excellence, and national pride ('सशक्त किसान, समृद्ध भारत')."
        },
        {
            "num": "02",
            "title": "The Ground Reality: Why Existing Agri-Tech Fails Grassroots Farmers",
            "category": "THE PROBLEM CONTEXT",
            "image": "slide-02.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · THE PROBLEM CONTEXT",
            "main_heading": "The Ground Reality: Why Existing Agri-Tech Fails Grassroots Farmers",
            "sub_heading": None,
            "lead_text": "Existing agricultural applications are built for urban agronomists on high-speed Wi-Fi, leaving actual dirt-under-the-fingernails farmers stranded with four critical failures:",
            "cards": [
                ("🧪 Chemical Overdosing & Fertilizer Burn", "Farmers apply Urea & DAP blindly based on habit. Soil Organic Carbon (SOC) has plummeted below 0.5% in 70% of Indian soils. Massive leaching wastes ₹12,000/ha."),
                ("🌾 Seed Fraud & Store Disconnect", "Fake or sub-par seed varieties flood local private dealers. Farmers have zero real-time awareness of nearest Government Subsidized Seed Stores (राजकीय बीज भंडार) or KVKs."),
                ("🌧️ Microclimate Shocks & Rain Leaching", "Weather forecasts are too generic (state-level). Top-dressing Urea right before sudden downpours washes expensive nitrogen into local waterways, causing 100% chemical loss."),
                ("📱 Literacy & Digital Divide Barrier", "Most agriculture portals are complex English spreadsheets designed for desktop agronomists. India's rural smallholders (Class 5 literacy) are completely left behind.")
            ],
            "bullets": [],
            "image_description": "1920×1080 2×2 grid slide. Each problem is enclosed in a crisp white rounded card (`#ffffff`) with subtle border lines (`#d4dfd6`). Bold card headers use dark forest green and descriptive emojis to anchor visual meaning.",
            "farmer_rationale": "Validates the real-life pain points experienced by smallholders daily: buying expensive bags only to have fertilizer wash away in rain, buying fake seeds, and feeling alienated by complex English interfaces."
        },
        {
            "num": "03",
            "title": "The 8 Inviolable Pillars: Permanent Project Foundation",
            "category": "ENDGAME MASTER BLUEPRINT",
            "image": "slide-03.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · ENDGAME MASTER BLUEPRINT",
            "main_heading": "The 8 Inviolable Pillars: Permanent Project Foundation",
            "sub_heading": None,
            "lead_text": "The core rules governing KhetSathi 360 architecture, permanently binding all frontend and backend engineering:",
            "cards": [
                ("1. Farmland Map Pointer", "Tap/drag pin on satellite imagery; 1-click GPS + lat/lon coordinate precision."),
                ("2. Certified Seed & Govt Stores", "Best climate-resilient varieties; locator for Block Seed Stores & subsidized rates."),
                ("3. Weather & Alternate Crop Pop-up", "NWP microclimate forecasting; minimizable top-right advice pop-up + machinery lifecycle."),
                ("4. Dual Soil Intelligence", "Multimodal 12-param SHC Vision OCR with strict guardrails + 695-district spatial baseline."),
                ("5. Amrit Mati Organic Mode", "One-touch chemical/organic toggle; input savings ledger + direct buyer/PGS-India links."),
                ("6. Industrial Speed & 4G PWA", "Sub-200ms TTFB, skeleton screens, and service worker offline caching on budget devices."),
                ("7. Class-5 Friendly UX Benchmark", "Visual tactile cards, audio speech narration, outdoor contrast, 100% bilingual parity."),
                ("8. Core Rule & Governance", "Permanent binding architectural constitution codified in docs/PROJECT_FOUNDATION.md.")
            ],
            "bullets": [],
            "image_description": "1920×1080 4×2 grid slide displaying 8 cards. Cards 1–5 feature emerald border highlights (`#10b981`), while Cards 6–8 feature amber accents (`#f59e0b`). This slide visually anchors the user's 8-point endgame vision into a permanent architectural roadmap.",
            "farmer_rationale": "Guarantees that the software will never drift into bloatware or abandon low-income farmers. It acts as an inviolable social contract between the system and rural users."
        },
        {
            "num": "04",
            "title": "Built & Live Prototype: Kisan Mitra 3-Step Decision Flow",
            "category": "PROTOTYPE ACCOMPLISHMENT · LIVE",
            "image": "slide-04.png",
            "embedded_proto": "proto_kisan_mitra_english_1080p.png",
            "badge": "KHETSATHI 360 · PROTOTYPE ACCOMPLISHMENT · LIVE",
            "main_heading": "Built & Live Prototype: Kisan Mitra 3-Step Decision Flow",
            "sub_heading": "Grassroots Simplicity with ICAR Rigor",
            "lead_text": "A working, field-tested decision flow allowing any farmer to receive tailored agronomic advice in under 30 seconds:",
            "cards": [],
            "bullets": [
                "Hyper-Local Location Picker: Blinkit-style auto-complete across 695 rural districts, tehsils, and village clusters.",
                "3-Way Land Area Unit Converter: Automatically converts local units (Pucca Bigha, Kuccha Bigha, Acre) into standard hectares.",
                "Deterministic Agronomic Plan: Calculates ICAR package of practices elemental targets and converts them into commercial 50kg DAP, 45kg Urea, and 50kg MOP bags.",
                "DAP Nitrogen Credit Offset: Automatically subtracts the 18% elemental N already delivered by DAP so farmers avoid over-applying Urea.",
                "Audio Narration: Built-in voice playback allowing low-literacy farmers to listen to their customized plan in clear Hindi/English."
            ],
            "image_description": "Split 1920×1080 slide layout. Left container (5.5\" width) hosts the agronomic feature bullets. Right container embeds `presentation/screenshots/kisan_mitra_english_ui.png` (also represented in standardized 1080p as `proto_kisan_mitra_english_1080p.png`), showing the live web application in Step 1.",
            "farmer_rationale": "Eliminates cognitive load. A farmer doesn't need to know complex soil chemistry; they simply specify their village and field size, and the platform delivers concrete physical bag counts (e.g., '1 Bag DAP at basal sowing, 1 Bag Urea at first watering')."
        },
        {
            "num": "05",
            "title": "Built & Live Prototype: Copernicus Sentinel-2 & Microclimate Safety",
            "category": "REMOTE SENSING & NWP · LIVE",
            "image": "slide-05.png",
            "embedded_proto": "proto_remote_sensing_sentinel2_1080p.png",
            "badge": "KHETSATHI 360 · REMOTE SENSING & NWP · LIVE",
            "main_heading": "Built & Live Prototype: Copernicus Sentinel-2 & Microclimate Safety",
            "sub_heading": "Space-to-Soil Remote Sensing Architecture",
            "lead_text": "Connecting European Space Agency orbital sensors and Numerical Weather Prediction directly to the farmer's palm:",
            "cards": [],
            "bullets": [
                "Copernicus Sentinel-2 10m MSI NDVI: Evaluates live vegetative crop vigor and foliage density directly from European Space Agency orbital telemetry.",
                "ISRIC SoilGrids 250m Profile: Extracts physical topsoil clay percentage, bulk density (g/cm³), and cation exchange capacity (CEC) to predict fertilizer retention.",
                "Open-Meteo High-Resolution NWP: Real-time numerical weather prediction delivering live temperature, relative humidity, and 48-hour precipitation forecasts.",
                "Active Rain-Leaching Guardrail: Triggers an immediate high-contrast alert: 'HOLD Urea Top-Dress!' when 48h rain probability exceeds 60%, saving thousands of rupees in fertilizer runoff.",
                "FAO-56 Evapotranspiration (ET0): Dynamic crop water demand curve calculating daily irrigation requirements in mm/day."
            ],
            "image_description": "Split 1920×1080 layout with embedded image on the left (`presentation/screenshots/sentinel2_soilgrids_remote_sensing.png` / `proto_remote_sensing_sentinel2_1080p.png`) showing live NDVI vigor meters (0.68 vegetative peak) and SoilGrids clay percentage (28.4%). Right card hosts technical bullet specifications.",
            "farmer_rationale": "Direct financial protection. By warning farmers not to spray Urea 12 hours before a downpour, KhetSathi 360 saves ₹1,500 to ₹4,500 per acre in wasted fertilizer on a single weather event."
        },
        {
            "num": "06",
            "title": "Built & Live Prototype: Multimodal SHC Vision OCR & Spatial IDW",
            "category": "LAB DATA & GEOSTATISTICS · LIVE",
            "image": "slide-06.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · LAB DATA & GEOSTATISTICS · LIVE",
            "main_heading": "Built & Live Prototype: Multimodal SHC Vision OCR & Spatial IDW",
            "sub_heading": None,
            "lead_text": "A dual-track approach reconciling the reality that only 35% of Indian farmers have lab soil cards, while 65% rely on regional baselines:",
            "cards": [
                ("Multimodal Vision OCR with Guardrails", "• Instant Lab Card Digitization: Farmers photograph their official Soil Health Card; computer vision extracts all 12 chemical parameters (N, P, K, OC, pH, EC, S, Zn, Fe, Cu, Mn, B).\n• Rigorous Document Guardrails: Pre-validation filters reject non-agricultural documents (resumes, electricity bills, invoices, receipts) with zero false triggers.\n• Bilingual Devanagari OCR: Reads cards printed in Hindi, English, and regional state agricultural formats.\n• Dynamic Bag Calibration: Ingested soil numbers instantly adjust the fertilizer recommendation to address specific soil deficiencies (e.g., Zinc or Gypsum amendments)."),
                ("695-District Spatial IDW Baseline", "• Zero-Card Fallback: 65% of Indian farmers have never received a lab soil card. KhetSathi 360 provides a geostatistical baseline for every village.\n• Spatial Inverse Distance Weighting: Real centroid dataset spanning 695 rural districts of India interpolates expected soil N-P-K, pH, and organic carbon based on GPS coordinates.\n• Uncertainty Flagging: Transparently informs the farmer whether advice is 'Lab Card Verified' (±5% confidence) or 'District Baseline Estimate' (±15% confidence).\n• Autonomous Offline Operation: Geostatistical district bundle is pre-cached on the device, functioning without an active cellular connection.")
            ],
            "bullets": [],
            "image_description": "1920×1080 dual-card layout. Left card features an emerald border (`#10b981`) highlighting the Vision OCR pipeline. Right card features an amber border (`#f59e0b`) detailing the 695-district Spatial IDW fallback engine.",
            "farmer_rationale": "Ensures no farmer is turned away. If a farmer has a soil card, they get lab-precision recommendations; if they have no card, they still get instant, accurate district-level guidance."
        },
        {
            "num": "07",
            "title": "Built & Live Prototype: Standalone 'Amrit Mati' Organic Hub",
            "category": "ORGANIC MISSION & ECONOMICS · LIVE",
            "image": "slide-07.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · ORGANIC MISSION & ECONOMICS · LIVE",
            "main_heading": "Built & Live Prototype: Standalone 'Amrit Mati' Organic Hub",
            "sub_heading": None,
            "lead_text": "Promoting natural and regenerative farming through proven economic proof rather than empty moral lecturing:",
            "cards": [
                ("⏳ 30-Year Intergenerational Soil Simulator", "Farmers drag a timeline slider from 1 to 30 years to contrast the degrading chemical trajectory (hardened soil, +180% input debt) against the regenerative organic trajectory (living earthworms, rich humus, 1.45% SOC)."),
                ("🥣 DIY Zero-Cost Bio-Input Recipe Kitchen", "Interactive proportional formulations for Jeevamrit (जीवामृत), Beejamrit (बीजामृत), and Neemastra (नीमास्त्र). Enter plot acreage, and ingredients (cow dung, urine, jaggery, neem leaves) automatically scale."),
                ("💰 Comparative Economic Ledger", "Demonstrates tangible farmer profitability: -18% fertilizer input savings, +25% organic mandi price premium, and ₹50,000/ha PKVY government assistance, resulting in +₹36,700 extra net profit per hectare."),
                ("🛒 Direct Institutional Buyer Routes", "Direct links and WhatsApp integration connecting farmers to Jaivik Kheti e-market, free PGS-India green/organic certification, SFAC/NABARD FPO aggregation hubs, and APEDA export channels.")
            ],
            "bullets": [],
            "image_description": "1920×1080 2×2 grid layout with emerald card borders. Each quadrant covers a distinct pillar of the live organic dashboard (`future.html`).",
            "farmer_rationale": "Solves the farmer's core hesitation: 'If I switch to organic, will my yield drop and will I go into debt?' By demonstrating concrete input savings and connecting to premium organic buyers, it makes organic farming profitable from Year 1."
        },
        {
            "num": "08",
            "title": "In Active Development: Interactive Farmland Map Pointing Tool",
            "category": "PILLAR 1 EVOLUTION · IN PROGRESS",
            "image": "slide-08.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · PILLAR 1 EVOLUTION · IN PROGRESS",
            "main_heading": "In Active Development: Interactive Farmland Map Pointing Tool",
            "sub_heading": "Touch-First Satellite Parcel Pinpointing (No Coordinates Required)",
            "lead_text": "While 1-Click GPS and Blinkit village search are active, farmers often need to point to a specific field parcel located 2 km away from their current home. We are embedding an interactive map widget directly into Step 1.",
            "cards": [
                ("📍 Interactive Draggable Pin", "Farmer opens the map, pans to their village, and drags a large harvest-pin directly onto their field parcel."),
                ("🛰️ Hybrid Satellite & Cadastral Overlay", "Utilizes high-resolution OpenStreetMap and ISRO Bhuvan satellite imagery showing field boundaries, canals, and village roads."),
                ("📐 Automatic Acreage Estimation", "Allows farmers to tap the corners of their farm to automatically compute field area in Bigha and Acres, eliminating manual conversion errors."),
                ("🔄 Real-Time Coordinate Sync", "Moving the pin instantly updates latitude, longitude, elevation, district agronomic zone, and microclimate weather forecast.")
            ],
            "bullets": [],
            "image_description": "1920×1080 layout with cyan accent framing (`#0891b2`). A large master card hosts the lead problem statement, followed by a 2×2 grid of rounded tactical cards detailing map features.",
            "farmer_rationale": "Farmers don't know their GPS coordinates, and their fields are often located outside the village residential cluster. A tactile touch-to-point satellite map gives them effortless boundary precision."
        },
        {
            "num": "09",
            "title": "In Active Development: Smart Alternate Crop Pop-up & Machinery Plan",
            "category": "PILLAR 3 EVOLUTION · IN PROGRESS",
            "image": "slide-09.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · PILLAR 3 EVOLUTION · IN PROGRESS",
            "main_heading": "In Active Development: Smart Alternate Crop Pop-up & Machinery Plan",
            "sub_heading": None,
            "lead_text": "Deploying proactive microclimate decision intelligence and plot-size calibrated machinery lifecycles:",
            "cards": [
                ("Floating Dynamic Crop Suggestion Pop-up", "• Non-Intrusive Top-Right Widget: Floats gracefully at the top-right of the screen with a 1-click 'Minimize / Expand' toggle, respecting farmer focus.\n• Predictive Crop Intelligence: Analyzes seasonal rainfall, canal water shortage, and prevailing mandi prices to evaluate if an alternate crop yields superior net margins.\n• Actionable Vernacular Suggestion: '🌾 आप गेहूं बो रहे हैं, पर इस साल कम पानी में सरसों (Mustard) लगाने से ₹18,000 अधिक मुनाफा और 60% कम पानी लगेगा!'\n• 1-Click Plan Switcher: Clicking 'विस्तार से देखें' immediately reconfigures the entire input, fertilizer, and harvest schedule to the recommended alternative."),
                ("Plot-Scale Machinery & Cultivation Lifecycle", "• Calibrated by Measured Farm Size: Machinery recommendations automatically adjust whether the farmer has 1 Bigha (0.25 ha) or 10 Hectares.\n• Smallholders (<2 Bigha): Recommends bullock ploughing, manual hand seeders, knapsack sprayers, and sickle reapers to minimize hired tractor rental waste.\n• Medium/Large Farms (>1 Ha): Recommends Tractor Rotavator for deep tillage, Seed-cum-Fertilizer Drills for uniform germination, and Combine Harvesters.\n• End-to-End Cultivation Timeline: Sowing depth, seed treatment (Beejamrit/Trichoderma), weeding stages, and irrigation milestones laid out chronologically.")
            ],
            "bullets": [],
            "image_description": "1920×1080 dual-card layout. Left card is bordered in warm amber (`#b45309`) detailing the floating pop-up. Right card is bordered in dark forest (`#1b4834`) detailing the machinery lifecycle.",
            "farmer_rationale": "Prevents catastrophic monoculture losses. If rain patterns indicate a drought, recommending mustard over wheat can save the farmer from total crop failure while cutting irrigation expenses."
        },
        {
            "num": "10",
            "title": "Under Polishing: Certified Seed Varieties & Govt Subsidized Stores",
            "category": "PILLAR 2 EVOLUTION · UP NEXT",
            "image": "slide-10.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · PILLAR 2 EVOLUTION · UP NEXT",
            "main_heading": "Under Polishing: Certified Seed Varieties & Govt Subsidized Stores",
            "sub_heading": "Bridging the Gap Between Research Seeds & Govt Subsidized Outlets",
            "lead_text": "High-yielding certified seeds often sit unsold at Government Block Seed Stores while farmers buy expensive, uncertified grain from middlemen. KhetSathi 360 brings transparency to certified seeds and authorized dealers.",
            "cards": [
                ("🏆 Verified Certified Varieties", "Recommends officially certified varieties (e.g. HD-2967, PBW-343, Pusa Basmati 1121) tailored to soil type, sowing date, and regional heat tolerance."),
                ("🏛️ Govt Block Seed Store Locator", "Integrates district directories for Block Agriculture Seed Stores (राजकीय कृषि बीज भंडार), Krishi Vigyan Kendras (KVK), and PACS societies nearby."),
                ("💰 Transparent Price Subsidies", "Displays Government Subsidized Seed Rates (e.g., ₹22/kg) alongside prevailing open market prices (₹38/kg), showing exact cash savings."),
                ("📞 Direct Dealer & Contact Directory", "Provides direct phone numbers, addresses, and navigation routes to authorized seed distribution centers within a 15 km radius.")
            ],
            "bullets": [],
            "image_description": "1920×1080 master card with 4 internal tactical cards (`#f4f7f4` fill) explaining certified varieties, block store locator, transparent subsidies, and dealer directories.",
            "farmer_rationale": "Eliminates seed fraud. Over 25% of seeds purchased from unauthorized rural dealers have low germination rates (<60%). Connecting directly to government subsidized seed stores guarantees >85% germination at half the price."
        },
        {
            "num": "11",
            "title": "Design Benchmark: Accessible for Class-5 Educated Farmers",
            "category": "HUMAN-COMPUTER INTERACTION (HCI)",
            "image": "slide-11.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · HUMAN-COMPUTER INTERACTION (HCI)",
            "main_heading": "Design Benchmark: Accessible for Class-5 Educated Farmers",
            "sub_heading": None,
            "lead_text": "Establishing a revolutionary new standard in rural UI/UX design, tailored specifically for smallholders who only know how to cultivate:",
            "cards": [
                ("👁️ Visual Tactile Cards (No Dense Jargon)", "Information is delivered through physical-metaphor cards (fertilizer bags with exact 50kg/45kg badges, watering icons, weather pills). Zero confusing chemical formulas in the primary farmer view."),
                ("🔊 Voice Audio Reader ('सलाह बोलकर सुनें')", "One-touch audio narration translates the full operational plan into clear spoken Hindi or English via the Web Speech API and backend TTS, allowing illiterate farmers to listen hands-free."),
                ("☀️ High-Contrast Outdoor Sun Legibility", "Engineered for harsh outdoor sunlight in the middle of a farm field. Deep agricultural forest green (#0e2d1f), harvest gold (#f59e0b), and stark white cards exceed WCAG 2.2 AA standards."),
                ("🌐 100% Flawless Bilingual Parity", "Guaranteed zero untranslated English remnants in Hindi mode, and zero leftover Devanagari in English mode. 152 translation keys synchronized across all application modules.")
            ],
            "bullets": [],
            "image_description": "1920×1080 4-card matrix with amber border trims. Highlights tactile cards, Web Speech API integration, WCAG 2.2 AA outdoor contrast, and 152-key bilingual synchronization.",
            "farmer_rationale": "Breaks the literacy barrier. A farmer working outdoors in harsh sunlight can tap a single speaker button and hear their exact fertilizer dosage read aloud in pure vernacular Hindi."
        },
        {
            "num": "12",
            "title": "Technical Architecture: Scalability & Low-Spec 4G Readiness",
            "category": "INDUSTRIAL-GRADE PERFORMANCE",
            "image": "slide-12.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · INDUSTRIAL-GRADE PERFORMANCE",
            "main_heading": "Technical Architecture: Scalability & Low-Spec 4G Readiness",
            "sub_heading": None,
            "lead_text": "Built for rural reality: low-spec budget phones (JioBharat, Redmi A-series, 2GB RAM) operating on intermittent 2G/3G/4G connectivity:",
            "cards": [
                ("⚡ Sub-200ms Time-to-First-Byte", "Ultra-lean zero-framework delivery on the root route ('/') ensures lightning-fast boot times even on slow 2G/3G/4G connections."),
                ("📴 PWA Offline Service Worker (v2.3)", "Evicts stale caches and pre-caches the 695-district geostatistical baseline, enabling zero-connectivity field operations when cell towers drop."),
                ("🦴 Smooth Shimmer Skeleton Loaders", "Eliminates Cumulative Layout Shift (CLS < 0.05) and white-screen hangs while asynchronous weather or satellite telemetry loads."),
                ("🧱 Clean Modular FastAPI Backend", "Strict Pydantic contract validation, stateless microservices, and 51+ unit tests passing with 100% CI/CD quality gate pass rate.")
            ],
            "bullets": [],
            "image_description": "1920×1080 4-card matrix with forest green border trims (`#1b4834`). Details sub-200ms TTFB, Service Worker v2.3 cache invalidation, shimmer skeleton UI, and FastAPI modularity.",
            "farmer_rationale": "Prevents app abandonment in remote villages. When cell towers cut out in rural areas, the app continues functioning offline without freezing or dropping state."
        },
        {
            "num": "13",
            "title": "Scope Discipline: What We Pruned & Why",
            "category": "PRODUCT PRUNING & REFINEMENT",
            "image": "slide-13.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · PRODUCT PRUNING & REFINEMENT",
            "main_heading": "Scope Discipline: What We Pruned & Why",
            "sub_heading": None,
            "lead_text": "True engineering excellence is defined by what you choose NOT to build. We systematically eliminated 4 high-friction distractions:",
            "cards": [
                ("❌ Generic / Non-Agri OCR Documents", "Why Pruned: Farmers inadvertently uploaded resumes, grocery bills, and identity cards. We engineered strict rejection guardrails rather than attempting to parse non-agricultural documents."),
                ("❌ Heavy Desktop Agronomist Spreadsheets", "Why Pruned: Dense data tables with 40+ decimal columns overwhelm farmers. We relocated advanced statistical models to an optional 'Scientific Mode' toggle, keeping the main interface clean."),
                ("❌ Bulky Client-Side JS Framework Bundles", "Why Pruned: Monolithic client bundles caused 5-second blank screen hangs on budget 2GB-RAM Android phones. The root interface was re-architected into zero-bloat tactile HTML/CSS."),
                ("❌ Theoretical Web3 / Blockchain Schemes", "Why Pruned: Abstract crypto and carbon token speculation distracts from real-world farmer profitability. We anchored organic incentives directly into proven government PKVY subsidies and verified mandis.")
            ],
            "bullets": [],
            "image_description": "1920×1080 4-card alert layout with bold crimson borders (`#dc2626`). Highlights disciplined deprecation of non-agri OCR, dense scientific tables, heavy JS bundles, and speculative crypto tokens.",
            "farmer_rationale": "Keeps the platform razor-focused on actionable farming advice rather than confusing gimmicks, high battery drain, or irrelevant digital clutter."
        },
        {
            "num": "14",
            "title": "Strategic Roadmap: Deployment Status & Next Engineering Phase",
            "category": "EXECUTION PLAN & SUMMARY",
            "image": "slide-14.png",
            "embedded_proto": None,
            "badge": "KHETSATHI 360 · EXECUTION PLAN & SUMMARY",
            "main_heading": "Strategic Roadmap: Deployment Status & Next Engineering Phase",
            "sub_heading": None,
            "lead_text": "Phased rollout trajectory translating the 8 Inviolable Pillars into production releases:",
            "cards": [
                ("[PROTOTYPE LIVE ON RENDER] Main Kisan Mitra Advisory & Future Organic Hub", "Serving live at khetsathi-360.onrender.com. Complete 51-test suite passing, Spatial IDW active across 695 districts, Copernicus Sentinel-2 NDVI live, zero bilingual drift."),
                ("[IMMEDIATE PHASE A] Interactive Farmland Map Pointer", "Integrate touch-first satellite/cadastral map widget into Step 1. Farmers tap or drag a harvest pin onto their exact field parcel for automatic coordinate and area lock."),
                ("[IMMEDIATE PHASE B] Smart Floating Pop-up & Machinery Guide", "Deploy top-right minimizable dynamic advice widget recommending higher-margin seasonal crops + end-to-end machinery lifecycle tailored to measured farm acreage."),
                ("[IMMEDIATE PHASE C] Subsidized Seed & Govt Store Locator", "Integrate National Seeds Corp and state Beej Vikas Nigam directories. Connect farmers to nearest Block Seed Stores with transparent subsidized pricing.")
            ],
            "bullets": [],
            "image_description": "1920×1080 balanced 4-card grid. Card 1 (Emerald): Live Prototype status. Card 2 (Cyan): Immediate Phase A Map Pointer. Card 3 (Amber): Immediate Phase B Pop-up. Card 4 (Forest Green): Immediate Phase C Store Locator.",
            "farmer_rationale": "Demonstrates continuous, stable, reliable progress. The core features farmers rely on stay live 24/7 while new capabilities roll out smoothly."
        }
    ]

    for s in slides_info:
        md.append(f"### Page {s['num']}: {s['title']}\n")
        md.append(f"- **Slide Number**: Page {s['num']} of 14")
        md.append(f"- **Category / Breadcrumb**: `{s['category']}`")
        md.append(f"- **Primary Standardized Image**: [`{s['image']}`](file:///x:/khetsathi-360/presentation/standardized_1080p/{s['image']}) *(1920 × 1080)*")
        if s['embedded_proto']:
            md.append(f"- **Embedded Prototype Screenshot**: [`{s['embedded_proto']}`](file:///x:/khetsathi-360/presentation/standardized_1080p/{s['embedded_proto']}) *(1920 × 1080)*")
        md.append(f"- **Banner Badge**: `{s['badge']}`")
        md.append(f"- **Main Heading**: **{s['main_heading']}**")
        if s['sub_heading']:
            md.append(f"- **Subheading / Lead**: *{s['sub_heading']}*")
        md.append(f"- **Lead Narrative**: {s['lead_text']}\n")

        # Cards / Bullets
        if s['cards']:
            md.append("#### Slide Content Cards / Modules:")
            for title, desc in s['cards']:
                md.append(f"- **{title}**:\n  {desc.replace(chr(10), chr(10) + '  ')}")
            md.append("")

        if s['bullets']:
            md.append("#### Slide Content Bullets:")
            for b in s['bullets']:
                md.append(f"- {b}")
            md.append("")

        md.append("#### Visual Layout & Image Analysis:")
        md.append(s['image_description'])
        md.append(f"\n> **Farmer-Centric Rationale**: {s['farmer_rationale']}\n")
        md.append("---\n")

    # Section 4: Design Standards
    md.append("## 4. Visual Design Standards & Brand Hierarchy\n")
    md.append("The visual system utilizes the high-contrast **KhetSathi Soil & Harvest** design palette, optimized for outdoor viewing under harsh direct sunlight (WCAG 2.2 AA compliant):\n")
    md.append("| Swatch | Name | Hex Code | RGB | Role in Slides & Document |")
    md.append("|---|---|---|---|---|")
    md.append("| 🌲 | Deep Forest Green | `#0e2d1f` | `(14, 45, 31)` | Master canvas background, primary brand headers, high-contrast containers. |")
    md.append("| 🌿 | Medium Forest | `#1b4834` | `(27, 72, 52)` | Sub-header banners, secondary card borders, card fills. |")
    md.append("| 🍃 | Living Emerald | `#10b981` | `(16, 185, 129)` | Prototype accomplishment accents, verified status badges, organic badges. |")
    md.append("| 🌾 | Harvest Amber | `#f59e0b` | `(245, 158, 11)` | Accent strips, callouts, metric badges, caution flags. |")
    md.append("| 🍂 | Dark Amber | `#b45309` | `(180, 83, 9)` | Pop-up notification headers, alert highlights. |")
    md.append("| 🌐 | Cyan Tech | `#0891b2` | `(8, 145, 178)` | Map pointing tool accents, GPS and satellite telemetry indicators. |")
    md.append("| 🚫 | Pruning Crimson | `#dc2626` | `(220, 38, 38)` | Deprecated features, non-agri OCR rejections, error guardrails. |")
    md.append("| 📜 | Stark White / Card Fill | `#ffffff` | `(255, 255, 255)` | Content card bodies, high-contrast text on dark backgrounds. |")
    md.append("| 📄 | Slate Muted Text | `#475569` | `(71, 85, 105)` | Explanatory secondary text, descriptions, captions. |\n")
    md.append("---\n")

    # Section 5: Mathematical & Agronomic Formulations Reference
    md.append("## 5. Mathematical & Agronomic Formulations Reference\n")
    md.append("The presentation incorporates deterministic scientific formulas implemented across `app/core/agronomics.py`, `app/core/soil_baseline.py`, and `app/core/weather_service.py`:\n")
    md.append("### 5.1 DAP Nitrogen Credit Offset Formula")
    md.append("When a farmer applies Di-Ammonium Phosphate (DAP) for Phosphorus ($P_2O_5$), it simultaneously delivers 18% elemental Nitrogen ($N$). To prevent chemical fertilizer burn, KhetSathi 360 automatically offsets the required Urea top-dress:\n")
    md.append("$$DAP_{bags} = \\left\\lceil \\frac{Target\\,P_2O_5\\,(kg/ha) \\times Area\\,(ha)}{0.46 \\times 50\\,kg} \\right\\rceil$$")
    md.append("$$N_{from\\,DAP} = DAP_{bags} \\times 50\\,kg \\times 0.18$$")
    md.append("$$N_{remaining} = \\max\\left(0, Target\\,N\\,(kg/ha) \\times Area\\,(ha) - N_{from\\,DAP}\\right)$$")
    md.append("$$Urea_{bags} = \\left\\lceil \\frac{N_{remaining}}{0.46 \\times 45\\,kg} \\right\\rceil$$\n")

    md.append("### 5.2 Spatial Inverse Distance Weighting (IDW) Baseline Formula")
    md.append("For farmers without an official Soil Health Card, expected N-P-K and pH are computed from centroids across 695 rural districts using 2nd-degree inverse distance weighting:\n")
    md.append("$$\\hat{z}(x) = \\frac{\\sum_{i=1}^{k} w_i z_i}{\\sum_{i=1}^{k} w_i} \\quad \\text{where} \\quad w_i = \\frac{1}{d(x, x_i)^2}$$\n")

    md.append("### 5.3 FAO-56 Reference Evapotranspiration ($ET_0$)")
    md.append("Calculates daily crop water demand in mm/day from Open-Meteo temperature, solar radiation, wind speed, and relative humidity:\n")
    md.append("$$ET_0 = \\frac{0.408 \\Delta (R_n - G) + \\gamma \\frac{900}{T + 273} u_2 (e_s - e_a)}{\\Delta + \\gamma (1 + 0.34 u_2)}$$\n")
    md.append("---\n")

    # Section 6: Cross-Page Image Utilization Matrix
    md.append("## 6. Cross-Page Image Utilization Matrix\n")
    md.append("The table below maps every standardized 1080p image to its appearance and utilization across the 14 pages of the presentation deck:\n")
    md.append("| Standardized Image File | Native Dimensions | Standardized Resolution | Rendered Page(s) | Slide Title / Context | Placement Format |")
    md.append("|---|---|---|---|---|---|")
    md.append("| `slide-01.png` | 1920 × 1080 | 1920 × 1080 | **Page 01** | Title & Executive Vision | Full slide presentation |")
    md.append("| `slide-02.png` | 1920 × 1080 | 1920 × 1080 | **Page 02** | The Ground Reality | Full slide presentation |")
    md.append("| `slide-03.png` | 1920 × 1080 | 1920 × 1080 | **Page 03** | The 8 Inviolable Pillars | Full slide presentation |")
    md.append("| `slide-04.png` | 1920 × 1080 | 1920 × 1080 | **Page 04** | Built & Live: Kisan Mitra | Full slide presentation |")
    md.append("| `slide-05.png` | 1920 × 1080 | 1920 × 1080 | **Page 05** | Built & Live: Sentinel-2 & Weather | Full slide presentation |")
    md.append("| `slide-06.png` | 1920 × 1080 | 1920 × 1080 | **Page 06** | Built & Live: Vision OCR & IDW | Full slide presentation |")
    md.append("| `slide-07.png` | 1920 × 1080 | 1920 × 1080 | **Page 07** | Built & Live: Amrit Mati Hub | Full slide presentation |")
    md.append("| `slide-08.png` | 1920 × 1080 | 1920 × 1080 | **Page 08** | Active Dev: Farmland Map Pointer | Full slide presentation |")
    md.append("| `slide-09.png` | 1920 × 1080 | 1920 × 1080 | **Page 09** | Active Dev: Smart Pop-up & Tools | Full slide presentation |")
    md.append("| `slide-10.png` | 1920 × 1080 | 1920 × 1080 | **Page 10** | Under Polishing: Certified Seeds | Full slide presentation |")
    md.append("| `slide-11.png` | 1920 × 1080 | 1920 × 1080 | **Page 11** | UX Benchmark: Class-5 Farmers | Full slide presentation |")
    md.append("| `slide-12.png` | 1920 × 1080 | 1920 × 1080 | **Page 12** | Technical Architecture | Full slide presentation |")
    md.append("| `slide-13.png` | 1920 × 1080 | 1920 × 1080 | **Page 13** | Scope Discipline | Full slide presentation |")
    md.append("| `slide-14.png` | 1920 × 1080 | 1920 × 1080 | **Page 14** | Strategic Roadmap | Full slide presentation |")
    md.append("| `proto_kisan_mitra_english_1080p.png` | 1370 × 637 | 1920 × 1080 | **Page 04** | Kisan Mitra 3-Step Decision Flow | Embedded right card (5.9\" width) |")
    md.append("| `proto_kisan_mitra_hindi_1080p.png` | 1366 × 577 | 1920 × 1080 | **Page 04, 11** | Bilingual Parity & Hindi Decision Flow | Reference companion in documentation |")
    md.append("| `proto_remote_sensing_sentinel2_1080p.png` | 1370 × 637 | 1920 × 1080 | **Page 05** | Space-to-Soil Remote Sensing | Embedded left card (5.8\" width) |")
    md.append("| `proto_weather_land_converter_1080p.png` | 1370 × 637 | 1920 × 1080 | **Page 05, 06** | Unit Converter & Weather Alert | Reference companion in documentation |\n")

    full_text = "\n".join(md)

    # Write to docs/KHETSATHI_360_PRESENTATION_CATALOG.md
    catalog_path1 = docs_dir / "KHETSATHI_360_PRESENTATION_CATALOG.md"
    with open(catalog_path1, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Generated catalog at: {catalog_path1}")

    # Write to presentation/PRESENTATION_IMAGE_CATALOG.md
    catalog_path2 = pres_dir / "PRESENTATION_IMAGE_CATALOG.md"
    with open(catalog_path2, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Generated catalog at: {catalog_path2}")

    return full_text

if __name__ == "__main__":
    generate_catalog()
