"""
scripts/generate_master_presentation.py
Generates a full-fledged, master-grade 14-slide PPTX presentation for KhetSathi 360.
Includes executive design, high-contrast palette, prototype screenshots, and detailed pillar roadmap.
"""

import os
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt


def create_deck():
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Brand Color Palette
    C_FOREST_DARK = RGBColor(14, 45, 31)  # #0e2d1f
    C_FOREST_MED = RGBColor(27, 72, 52)  # #1b4834
    C_EMERALD = RGBColor(16, 185, 129)  # #10b981
    C_AMBER = RGBColor(245, 158, 11)  # #f59e0b
    C_AMBER_DARK = RGBColor(180, 83, 9)  # #b45309
    C_SLATE_DARK = RGBColor(15, 31, 23)  # #0f1f17
    C_SLATE_MUTED = RGBColor(71, 85, 105)  # #475569
    C_LIGHT_BG = RGBColor(244, 247, 244)  # #f4f7f4
    C_WHITE = RGBColor(255, 255, 255)  # #ffffff
    C_CARD_BORDER = RGBColor(212, 223, 214)  # #d4dfd6
    C_CYAN = RGBColor(8, 145, 178)  # #0891b2
    C_RED = RGBColor(220, 38, 38)  # #dc2626

    def add_header(slide, title_text, category_text="KHETSATHI 360 · STRATEGIC BLUEPRINT"):
        # Header banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_FOREST_DARK
        top_bar.line.color.rgb = C_FOREST_MED

        # Category / breadcrumb
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        p_cat = tb_cat.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_EMERALD

        # Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.65))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Bottom accent strip
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.05))
        accent.fill.solid()
        accent.fill.fore_color.rgb = C_AMBER
        accent.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: COVER / TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_FOREST_DARK
    bg1.line.fill.background()

    s1_accent = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    s1_accent.fill.solid()
    s1_accent.fill.fore_color.rgb = C_FOREST_MED
    s1_accent.line.color.rgb = C_EMERALD
    s1_accent.line.width = Pt(2)

    tb1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.4), Inches(10.7), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "🌾 NATIONAL DIGITAL AGRI DECISION PLATFORM · राष्ट्रीय डिजिटल कृषि निर्णय प्रणाली"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = C_AMBER

    p_main = tf1.add_paragraph()
    p_main.text = "KhetSathi 360"
    p_main.font.size = Pt(46)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE

    p_sub = tf1.add_paragraph()
    p_sub.text = "Endgame Master Architecture & Prototype Presentation"
    p_sub.font.size = Pt(22)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_EMERALD

    p_desc = tf1.add_paragraph()
    p_desc.text = "From Farmland Map Pointing & Certified Seeds to Space Remote Sensing, Soil Regeneration & Direct Mandi Markets — Built for 140 Million Grassroots Indian Farmers."
    p_desc.font.size = Pt(14)
    p_desc.font.color.rgb = RGBColor(220, 240, 230)

    pill_data = [
        ("695 Districts", "Full Pan-India Geospatial Baseline"),
        ("Class-5 UX", "Visual Cards + Audio Speech Reader"),
        ("100% Parity", "Flawless Bilingual Hindi ⇄ English"),
    ]
    for idx, (title, sub) in enumerate(pill_data):
        card_x = Inches(1.3 + idx * 3.65)
        add_card(s1, card_x, Inches(4.8), Inches(3.4), Inches(1.3), bg_color=C_FOREST_DARK, border_color=C_AMBER)
        tb = s1.shapes.add_textbox(card_x, Inches(4.85), Inches(3.4), Inches(1.2))
        p1 = tb.text_frame.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = C_AMBER
        p2 = tb.text_frame.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: THE GROUND REALITY (PROBLEM STATEMENT)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Ground Reality: Why Existing Agri-Tech Fails Grassroots Farmers", "THE PROBLEM CONTEXT")

    problems = [
        (
            "🧪 Chemical Overdosing & Fertilizer Burn",
            "Farmers apply Urea & DAP blindly based on habit. Soil Organic Carbon (SOC) has plummeted below 0.5% in 70% of Indian soils. Massive leaching wastes ₹12,000/ha.",
        ),
        (
            "🌾 Seed Fraud & Store Disconnect",
            "Fake or sub-par seed varieties flood local private dealers. Farmers have zero real-time awareness of nearest Government Subsidized Seed Stores (राजकीय बीज भंडार) or KVKs.",
        ),
        (
            "🌧️ Microclimate Shocks & Rain Leaching",
            "Weather forecasts are too generic (state-level). Top-dressing Urea right before sudden downpours washes expensive nitrogen into local waterways, causing 100% chemical loss.",
        ),
        (
            "📱 Literacy & Digital Divide Barrier",
            "Most agriculture portals are complex English spreadsheets designed for desktop agronomists. India's rural smallholders (Class 5 literacy) are completely left behind.",
        ),
    ]
    for i, (title, desc) in enumerate(problems):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 6.0)
        cy = Inches(1.5 + row * 2.7)
        add_card(s2, cx, cy, Inches(5.7), Inches(2.4), bg_color=C_WHITE, border_color=C_CARD_BORDER)
        tb = s2.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), Inches(5.1), Inches(2.0))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_FOREST_DARK
        p2 = tb.text_frame.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 3: THE 8 INVIOLABLE PILLARS (CORE FOUNDATION)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The 8 Inviolable Pillars: Permanent Project Foundation", "ENDGAME MASTER BLUEPRINT")

    pillars = [
        ("1. Farmland Map Pointer", "Tap/drag pin on satellite imagery; 1-click GPS + lat/lon coordinate precision."),
        (
            "2. Certified Seed & Govt Stores",
            "Best climate-resilient varieties; locator for Block Seed Stores & subsidized rates.",
        ),
        (
            "3. Weather & Alternate Crop Pop-up",
            "NWP microclimate forecasting; minimizable top-right advice pop-up + machinery lifecycle.",
        ),
        (
            "4. Dual Soil Intelligence",
            "Multimodal 12-param SHC Vision OCR with strict guardrails + 695-district spatial baseline.",
        ),
        (
            "5. Amrit Mati Organic Mode",
            "One-touch chemical/organic toggle; input savings ledger + direct buyer/PGS-India links.",
        ),
        (
            "6. Industrial Speed & 4G PWA",
            "Sub-200ms TTFB, skeleton screens, and service worker offline caching on budget devices.",
        ),
        (
            "7. Class-5 Friendly UX Benchmark",
            "Visual tactile cards, audio speech narration, outdoor contrast, 100% bilingual parity.",
        ),
        (
            "8. Core Rule & Governance",
            "Permanent binding architectural constitution codified in docs/PROJECT_FOUNDATION.md.",
        ),
    ]
    for i, (p_title, p_desc) in enumerate(pillars):
        row = i // 4
        col = i % 4
        cx = Inches(0.8 + col * 2.95)
        cy = Inches(1.5 + row * 2.7)
        add_card(s3, cx, cy, Inches(2.8), Inches(2.45), bg_color=C_WHITE, border_color=C_EMERALD if i < 5 else C_AMBER)
        tb = s3.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.15), Inches(2.5), Inches(2.15))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_FOREST_DARK
        p2 = tb.text_frame.add_paragraph()
        p2.text = p_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 4: PROTOTYPE 1 - KISAN MITRA DECISION ENGINE (LIVE)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Built & Live Prototype: Kisan Mitra 3-Step Decision Flow", "PROTOTYPE ACCOMPLISHMENT · LIVE")

    add_card(s4, Inches(0.8), Inches(1.45), Inches(5.5), Inches(5.6), bg_color=C_WHITE)
    tb4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.1), Inches(5.2))
    tb4.text_frame.word_wrap = True
    p = tb4.text_frame.paragraphs[0]
    p.text = "Grassroots Simplicity with ICAR Rigor"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    bullets4 = [
        "Hyper-Local Location Picker: Blinkit-style auto-complete across 695 rural districts, tehsils, and village clusters.",
        "3-Way Land Area Unit Converter: Automatically converts local units (Pucca Bigha, Kuccha Bigha, Acre) into standard hectares.",
        "Deterministic Agronomic Plan: Calculates ICAR package of practices elemental targets and converts them into commercial 50kg DAP, 45kg Urea, and 50kg MOP bags.",
        "DAP Nitrogen Credit Offset: Automatically subtracts the 18% elemental N already delivered by DAP so farmers avoid over-applying Urea.",
        "Audio Narration: Built-in voice playback allowing low-literacy farmers to listen to their customized plan in clear Hindi/English.",
    ]
    for b in bullets4:
        p_b = tb4.text_frame.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_SLATE_MUTED

    img_path1 = "presentation/screenshots/kisan_mitra_english_ui.png"
    if os.path.exists(img_path1):
        s4.shapes.add_picture(img_path1, Inches(6.6), Inches(1.45), width=Inches(5.9))

    # =========================================================================
    # SLIDE 5: PROTOTYPE 2 - REMOTE SENSING & WEATHER GUARDRAILS (LIVE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Built & Live Prototype: Copernicus Sentinel-2 & Microclimate Safety", "REMOTE SENSING & NWP · LIVE")

    img_path2 = "presentation/screenshots/sentinel2_soilgrids_remote_sensing.png"
    if os.path.exists(img_path2):
        s5.shapes.add_picture(img_path2, Inches(0.8), Inches(1.45), width=Inches(5.8))

    add_card(s5, Inches(6.9), Inches(1.45), Inches(5.6), Inches(5.6), bg_color=C_WHITE)
    tb5 = s5.shapes.add_textbox(Inches(7.1), Inches(1.6), Inches(5.2), Inches(5.2))
    tb5.text_frame.word_wrap = True
    p = tb5.text_frame.paragraphs[0]
    p.text = "Space-to-Soil Remote Sensing Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    bullets5 = [
        "Copernicus Sentinel-2 10m MSI NDVI: Evaluates live vegetative crop vigor and foliage density directly from European Space Agency orbital telemetry.",
        "ISRIC SoilGrids 250m Profile: Extracts physical topsoil clay percentage, bulk density (g/cm³), and cation exchange capacity (CEC) to predict fertilizer retention.",
        "Open-Meteo High-Resolution NWP: Real-time numerical weather prediction delivering live temperature, relative humidity, and 48-hour precipitation forecasts.",
        "Active Rain-Leaching Guardrail: Triggers an immediate high-contrast alert: 'HOLD Urea Top-Dress!' when 48h rain probability exceeds 60%, saving thousands of rupees in fertilizer runoff.",
        "FAO-56 Evapotranspiration (ET0): Dynamic crop water demand curve calculating daily irrigation requirements in mm/day.",
    ]
    for b in bullets5:
        p_b = tb5.text_frame.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 6: PROTOTYPE 3 - SOIL HEALTH CARD OCR & SPATIAL IDW (LIVE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Built & Live Prototype: Multimodal SHC Vision OCR & Spatial IDW", "LAB DATA & GEOSTATISTICS · LIVE")

    add_card(s6, Inches(0.8), Inches(1.45), Inches(5.7), Inches(5.6), bg_color=C_WHITE, border_color=C_EMERALD)
    tb6a = s6.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tb6a.text_frame.word_wrap = True
    p = tb6a.text_frame.paragraphs[0]
    p.text = "Multimodal Vision OCR with Guardrails"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    b6a = [
        "Instant Lab Card Digitization: Farmers photograph their official Soil Health Card; computer vision extracts all 12 chemical parameters (N, P, K, OC, pH, EC, S, Zn, Fe, Cu, Mn, B).",
        "Rigorous Document Guardrails: Pre-validation filters reject non-agricultural documents (resumes, electricity bills, invoices, receipts) with zero false triggers.",
        "Bilingual Devanagari OCR: Reads cards printed in Hindi, English, and regional state agricultural formats.",
        "Dynamic Bag Calibration: Ingested soil numbers instantly adjust the fertilizer recommendation to address specific soil deficiencies (e.g., Zinc or Gypsum amendments).",
    ]
    for b in b6a:
        p_b = tb6a.text_frame.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_SLATE_MUTED

    add_card(s6, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.6), bg_color=C_WHITE, border_color=C_AMBER)
    tb6b = s6.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tb6b.text_frame.word_wrap = True
    p = tb6b.text_frame.paragraphs[0]
    p.text = "695-District Spatial IDW Baseline"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    b6b = [
        "Zero-Card Fallback: 65% of Indian farmers have never received a lab soil card. KhetSathi 360 provides a geostatistical baseline for every village.",
        "Spatial Inverse Distance Weighting: Real centroid dataset spanning 695 rural districts of India interpolates expected soil N-P-K, pH, and organic carbon based on GPS coordinates.",
        "Uncertainty Flagging: Transparently informs the farmer whether advice is 'Lab Card Verified' (±5% confidence) or 'District Baseline Estimate' (±15% confidence).",
        "Autonomous Offline Operation: Geostatistical district bundle is pre-cached on the device, functioning without an active cellular connection.",
    ]
    for b in b6b:
        p_b = tb6b.text_frame.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 7: PROTOTYPE 4 - AMRIT MATI ORGANIC FARMING HUB (LIVE)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Built & Live Prototype: Standalone 'Amrit Mati' Organic Hub", "ORGANIC MISSION & ECONOMICS · LIVE")

    features7 = [
        (
            "⏳ 30-Year Intergenerational Soil Simulator",
            "Farmers drag a timeline slider from 1 to 30 years to contrast the degrading chemical trajectory (hardened soil, +180% input debt) against the regenerative organic trajectory (living earthworms, rich humus, 1.45% SOC).",
        ),
        (
            "🥣 DIY Zero-Cost Bio-Input Recipe Kitchen",
            "Interactive proportional formulations for Jeevamrit (जीवामृत), Beejamrit (बीजामृत), and Neemastra (नीमास्त्र). Enter plot acreage, and ingredients (cow dung, urine, jaggery, neem leaves) automatically scale.",
        ),
        (
            "💰 Comparative Economic Ledger",
            "Demonstrates tangible farmer profitability: -18% fertilizer input savings, +25% organic mandi price premium, and ₹50,000/ha PKVY government assistance, resulting in +₹36,700 extra net profit per hectare.",
        ),
        (
            "🛒 Direct Institutional Buyer Routes",
            "Direct links and WhatsApp integration connecting farmers to Jaivik Kheti e-market, free PGS-India green/organic certification, SFAC/NABARD FPO aggregation hubs, and APEDA export channels.",
        ),
    ]
    for i, (title, desc) in enumerate(features7):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 6.0)
        cy = Inches(1.5 + row * 2.7)
        add_card(s7, cx, cy, Inches(5.7), Inches(2.4), bg_color=C_WHITE, border_color=C_EMERALD)
        tb = s7.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), Inches(5.1), Inches(2.0))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_FOREST_DARK
        p2 = tb.text_frame.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 8: IN ACTIVE DEVELOPMENT - FARMLAND MAP POINTER
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "In Active Development: Interactive Farmland Map Pointing Tool", "PILLAR 1 EVOLUTION · IN PROGRESS")

    add_card(s8, Inches(0.8), Inches(1.45), Inches(11.733), Inches(5.6), bg_color=C_WHITE, border_color=C_CYAN)
    tb8 = s8.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.1), Inches(5.2))
    tb8.text_frame.word_wrap = True
    p = tb8.text_frame.paragraphs[0]
    p.text = "Touch-First Satellite Parcel Pinpointing (No Coordinates Required)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    p_lead = tb8.text_frame.add_paragraph()
    p_lead.text = "While 1-Click GPS and Blinkit village search are active, farmers often need to point to a specific field parcel located 2 km away from their current home. We are embedding an interactive map widget directly into Step 1."
    p_lead.font.size = Pt(13)
    p_lead.font.color.rgb = C_SLATE_MUTED

    dev_points = [
        (
            "📍 Interactive Draggable Pin",
            "Farmer opens the map, pans to their village, and drags a large harvest-pin directly onto their field parcel.",
        ),
        (
            "🛰️ Hybrid Satellite & Cadastral Overlay",
            "Utilizes high-resolution OpenStreetMap and ISRO Bhuvan satellite imagery showing field boundaries, canals, and village roads.",
        ),
        (
            "📐 Automatic Acreage Estimation",
            "Allows farmers to tap the corners of their farm to automatically compute field area in Bigha and Acres, eliminating manual conversion errors.",
        ),
        (
            "🔄 Real-Time Coordinate Sync",
            "Moving the pin instantly updates latitude, longitude, elevation, district agronomic zone, and microclimate weather forecast.",
        ),
    ]
    for idx, (head, body) in enumerate(dev_points):
        row = idx // 2
        col = idx % 2
        cx = Inches(1.1 + col * 5.6)
        cy = Inches(3.2 + row * 1.8)
        add_card(s8, cx, cy, Inches(5.3), Inches(1.6), bg_color=C_LIGHT_BG, border_color=C_CARD_BORDER)
        tb_sub = s8.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.15), Inches(4.9), Inches(1.3))
        tb_sub.text_frame.word_wrap = True
        p1 = tb_sub.text_frame.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN
        p2 = tb_sub.text_frame.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_SLATE_DARK

    # =========================================================================
    # SLIDE 9: IN ACTIVE DEVELOPMENT - SMART POP-UP & MACHINERY GUIDE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(
        s9, "In Active Development: Smart Alternate Crop Pop-up & Machinery Plan", "PILLAR 3 EVOLUTION · IN PROGRESS"
    )

    add_card(s9, Inches(0.8), Inches(1.45), Inches(5.7), Inches(5.6), bg_color=C_WHITE, border_color=C_AMBER)
    tb9a = s9.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tb9a.text_frame.word_wrap = True
    p = tb9a.text_frame.paragraphs[0]
    p.text = "Floating Dynamic Crop Suggestion Pop-up"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_DARK

    b9a = [
        "Non-Intrusive Top-Right Widget: Floats gracefully at the top-right of the screen with a 1-click 'Minimize / Expand' toggle, respecting farmer focus.",
        "Predictive Crop Intelligence: Analyzes seasonal rainfall, canal water shortage, and prevailing mandi prices to evaluate if an alternate crop yields superior net margins.",
        "Actionable Vernacular Suggestion: '🌾 आप गेहूं बो रहे हैं, पर इस साल कम पानी में सरसों (Mustard) लगाने से ₹18,000 अधिक मुनाफा और 60% कम पानी लगेगा!'",
        "1-Click Plan Switcher: Clicking 'विस्तार से देखें' immediately reconfigures the entire input, fertilizer, and harvest schedule to the recommended alternative.",
    ]
    for b in b9a:
        p_b = tb9a.text_frame.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_SLATE_MUTED

    add_card(s9, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.6), bg_color=C_WHITE, border_color=C_FOREST_MED)
    tb9b = s9.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tb9b.text_frame.word_wrap = True
    p = tb9b.text_frame.paragraphs[0]
    p.text = "Plot-Scale Machinery & Cultivation Lifecycle"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    b9b = [
        "Calibrated by Measured Farm Size: Machinery recommendations automatically adjust whether the farmer has 1 Bigha (0.25 ha) or 10 Hectares.",
        "Smallholders (<2 Bigha): Recommends bullock ploughing, manual hand seeders, knapsack sprayers, and sickle reapers to minimize hired tractor rental waste.",
        "Medium/Large Farms (>1 Ha): Recommends Tractor Rotavator for deep tillage, Seed-cum-Fertilizer Drills for uniform germination, and Combine Harvesters.",
        "End-to-End Cultivation Timeline: Sowing depth, seed treatment (Beejamrit/Trichoderma), weeding stages, and irrigation milestones laid out chronologically.",
    ]
    for b in b9b:
        p_b = tb9b.text_frame.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 10: UNDER POLISHING - CERTIFIED SEEDS & GOVT STORES
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(
        s10, "Under Polishing: Certified Seed Varieties & Govt Subsidized Stores", "PILLAR 2 EVOLUTION · UP NEXT"
    )

    add_card(s10, Inches(0.8), Inches(1.45), Inches(11.733), Inches(5.6), bg_color=C_WHITE)
    tb10 = s10.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.1), Inches(5.2))
    tb10.text_frame.word_wrap = True
    p = tb10.text_frame.paragraphs[0]
    p.text = "Bridging the Gap Between Research Seeds & Govt Subsidized Outlets"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_FOREST_DARK

    p_lead10 = tb10.text_frame.add_paragraph()
    p_lead10.text = "High-yielding certified seeds often sit unsold at Government Block Seed Stores while farmers buy expensive, uncertified grain from middlemen. KhetSathi 360 brings transparency to certified seeds and authorized dealers."
    p_lead10.font.size = Pt(13)
    p_lead10.font.color.rgb = C_SLATE_MUTED

    seed_pillars = [
        (
            "🏆 Verified Certified Varieties",
            "Recommends officially certified varieties (e.g. HD-2967, PBW-343, Pusa Basmati 1121) tailored to soil type, sowing date, and regional heat tolerance.",
        ),
        (
            "🏛️ Govt Block Seed Store Locator",
            "Integrates district directories for Block Agriculture Seed Stores (राजकीय कृषि बीज भंडार), Krishi Vigyan Kendras (KVK), and PACS societies nearby.",
        ),
        (
            "💰 Transparent Price Subsidies",
            "Displays Government Subsidized Seed Rates (e.g., ₹22/kg) alongside prevailing open market prices (₹38/kg), showing exact cash savings.",
        ),
        (
            "📞 Direct Dealer & Contact Directory",
            "Provides direct phone numbers, addresses, and navigation routes to authorized seed distribution centers within a 15 km radius.",
        ),
    ]
    for idx, (head, body) in enumerate(seed_pillars):
        row = idx // 2
        col = idx % 2
        cx = Inches(1.1 + col * 5.6)
        cy = Inches(3.2 + row * 1.8)
        add_card(s10, cx, cy, Inches(5.3), Inches(1.6), bg_color=C_LIGHT_BG, border_color=C_CARD_BORDER)
        tb_sub = s10.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.15), Inches(4.9), Inches(1.3))
        tb_sub.text_frame.word_wrap = True
        p1 = tb_sub.text_frame.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_FOREST_MED
        p2 = tb_sub.text_frame.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_SLATE_DARK

    # =========================================================================
    # SLIDE 11: CLASS-5 UX BENCHMARK (DESIGN & ACCESSIBILITY)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Design Benchmark: Accessible for Class-5 Educated Farmers", "HUMAN-COMPUTER INTERACTION (HCI)")

    hci_cards = [
        (
            "👁️ Visual Tactile Cards (No Dense Jargon)",
            "Information is delivered through physical-metaphor cards (fertilizer bags with exact 50kg/45kg badges, watering icons, weather pills). Zero confusing chemical formulas in the primary farmer view.",
        ),
        (
            "🔊 Voice Audio Reader ('सलाह बोलकर सुनें')",
            "One-touch audio narration translates the full operational plan into clear spoken Hindi or English via the Web Speech API and backend TTS, allowing illiterate farmers to listen hands-free.",
        ),
        (
            "☀️ High-Contrast Outdoor Sun Legibility",
            "Engineered for harsh outdoor sunlight in the middle of a farm field. Deep agricultural forest green (#0e2d1f), harvest gold (#f59e0b), and stark white cards exceed WCAG 2.2 AA standards.",
        ),
        (
            "🌐 100% Flawless Bilingual Parity",
            "Guaranteed zero untranslated English remnants in Hindi mode, and zero leftover Devanagari in English mode. 152 translation keys synchronized across all application modules.",
        ),
    ]
    for i, (title, desc) in enumerate(hci_cards):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 6.0)
        cy = Inches(1.5 + row * 2.7)
        add_card(s11, cx, cy, Inches(5.7), Inches(2.4), bg_color=C_WHITE, border_color=C_AMBER)
        tb = s11.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), Inches(5.1), Inches(2.0))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_FOREST_DARK
        p2 = tb.text_frame.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 12: TECHNICAL ARCHITECTURE & PERFORMANCE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Technical Architecture: Scalability & Low-Spec 4G Readiness", "INDUSTRIAL-GRADE PERFORMANCE")

    tech_points = [
        (
            "⚡ Sub-200ms Time-to-First-Byte",
            "Ultra-lean zero-framework delivery on the root route ('/') ensures lightning-fast boot times even on slow 2G/3G/4G connections.",
        ),
        (
            "📴 PWA Offline Service Worker (v2.3)",
            "Evicts stale caches and pre-caches the 695-district geostatistical baseline, enabling zero-connectivity field operations when cell towers drop.",
        ),
        (
            "🦴 Smooth Shimmer Skeleton Loaders",
            "Eliminates Cumulative Layout Shift (CLS < 0.05) and white-screen hangs while asynchronous weather or satellite telemetry loads.",
        ),
        (
            "🧱 Clean Modular FastAPI Backend",
            "Strict Pydantic contract validation, stateless microservices, and 51+ unit tests passing with 100% CI/CD quality gate pass rate.",
        ),
    ]
    for i, (title, desc) in enumerate(tech_points):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 6.0)
        cy = Inches(1.5 + row * 2.7)
        add_card(s12, cx, cy, Inches(5.7), Inches(2.4), bg_color=C_WHITE, border_color=C_FOREST_MED)
        tb = s12.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), Inches(5.1), Inches(2.0))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_FOREST_DARK
        p2 = tb.text_frame.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 13: PRUNED & SCOPE-TRIMMED ITEMS (DISCIPLINED ENGINEERING)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Scope Discipline: What We Pruned & Why", "PRODUCT PRUNING & REFINEMENT")

    pruned_items = [
        (
            "❌ Generic / Non-Agri OCR Documents",
            "Why Pruned: Farmers inadvertently uploaded resumes, grocery bills, and identity cards. We engineered strict rejection guardrails rather than attempting to parse non-agricultural documents.",
        ),
        (
            "❌ Heavy Desktop Agronomist Spreadsheets",
            "Why Pruned: Dense data tables with 40+ decimal columns overwhelm farmers. We relocated advanced statistical models to an optional 'Scientific Mode' toggle, keeping the main interface clean.",
        ),
        (
            "❌ Bulky Client-Side JS Framework Bundles",
            "Why Pruned: Monolithic client bundles caused 5-second blank screen hangs on budget 2GB-RAM Android phones. The root interface was re-architected into zero-bloat tactile HTML/CSS.",
        ),
        (
            "❌ Theoretical Web3 / Blockchain Schemes",
            "Why Pruned: Abstract crypto and carbon token speculation distracts from real-world farmer profitability. We anchored organic incentives directly into proven government PKVY subsidies and verified mandis.",
        ),
    ]
    for i, (title, desc) in enumerate(pruned_items):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 6.0)
        cy = Inches(1.5 + row * 2.7)
        add_card(s13, cx, cy, Inches(5.7), Inches(2.4), bg_color=C_WHITE, border_color=C_RED)
        tb = s13.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), Inches(5.1), Inches(2.0))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_RED
        p2 = tb.text_frame.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_SLATE_MUTED

    # =========================================================================
    # SLIDE 14: ROADMAP, DEPLOYED STATUS & NEXT EXECUTION
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Strategic Roadmap: Deployment Status & Next Engineering Phase", "EXECUTION PLAN & SUMMARY")

    phases14 = [
        (
            "PROTOTYPE LIVE ON RENDER",
            "Main Kisan Mitra Advisory & Future Organic Hub",
            "Serving live at khetsathi-360.onrender.com. Complete 51-test suite passing, Spatial IDW active across 695 districts, Copernicus Sentinel-2 NDVI live, zero bilingual drift.",
            C_EMERALD,
        ),
        (
            "IMMEDIATE PHASE A",
            "Interactive Farmland Map Pointer",
            "Integrate touch-first satellite/cadastral map widget into Step 1. Farmers tap or drag a harvest pin onto their exact field parcel for automatic coordinate and area lock.",
            C_CYAN,
        ),
        (
            "IMMEDIATE PHASE B",
            "Smart Floating Pop-up & Machinery Guide",
            "Deploy top-right minimizable dynamic advice widget recommending higher-margin seasonal crops + end-to-end machinery lifecycle tailored to measured farm acreage.",
            C_AMBER_DARK,
        ),
        (
            "IMMEDIATE PHASE C",
            "Subsidized Seed & Govt Store Locator",
            "Integrate National Seeds Corp and state Beej Vikas Nigam directories. Connect farmers to nearest Block Seed Stores with transparent subsidized pricing.",
            C_FOREST_MED,
        ),
    ]
    for idx, (badge, title, desc, border_c) in enumerate(phases14):
        row = idx // 2
        col = idx % 2
        cx = Inches(0.8 + col * 6.0)
        cy = Inches(1.5 + row * 2.7)
        add_card(s14, cx, cy, Inches(5.7), Inches(2.4), bg_color=C_WHITE, border_color=border_c)
        tb = s14.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.18), Inches(5.1), Inches(2.05))
        tb.text_frame.word_wrap = True

        p_b = tb.text_frame.paragraphs[0]
        p_b.text = f"[{badge}]"
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = border_c

        p_t = tb.text_frame.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = C_FOREST_DARK

        p_d = tb.text_frame.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_SLATE_MUTED

    # Save presentation
    out_dir = Path("presentation")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "KhetSathi_360_Master_Product_Blueprint.pptx"
    prs.save(str(out_path))
    print(f"Master presentation successfully generated at: {out_path}")
    print(f"File size: {out_path.stat().st_size} bytes")


if __name__ == "__main__":
    create_deck()
