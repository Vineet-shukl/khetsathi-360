import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import datetime

# Create Workbook
wb = openpyxl.Workbook()
# Default sheet
ws_dash = wb.active
ws_dash.title = "PROJECT DASHBOARD"
ws_tracker = wb.create_sheet(title="WORK TRACKER")

# Enable grid lines for both sheets
ws_dash.views.sheetView[0].showGridLines = True
ws_tracker.views.sheetView[0].showGridLines = True

# Define Color Palette (Theme: Professional AgriTech / 1M1B Green)
DARK_GREEN = "1E4B27"       # Primary header
FOREST_GREEN = "2D6A4F"     # Section headers
MINT_LIGHT = "E8F5E9"       # KPI background / light green
MINT_BORDER = "A5D6A7"
WHITE = "FFFFFF"
GRAY_TEXT = "555555"
LIGHT_GRAY_FILL = "F8F9FA"
BORDER_GRAY = "D0D5DD"

STATUS_COMPLETED_FILL = "D1E7DD"
STATUS_COMPLETED_TEXT = "0F5132"
STATUS_IN_PROGRESS_FILL = "CFF4FC"
STATUS_IN_PROGRESS_TEXT = "055160"
STATUS_PENDING_FILL = "FFF3CD"
STATUS_PENDING_TEXT = "664D03"

# Common Fonts
font_title = Font(name="Segoe UI", size=16, bold=True, color=WHITE)
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="E0E0E0")
font_sec_hdr = Font(name="Segoe UI", size=11, bold=True, color=WHITE)
font_tbl_hdr = Font(name="Segoe UI", size=10, bold=True, color=WHITE)
font_bold = Font(name="Segoe UI", size=10, bold=True)
font_kpi_label = Font(name="Segoe UI", size=9, bold=True, color="2D6A4F")
font_kpi_val = Font(name="Segoe UI", size=18, bold=True, color="1E4B27")
font_regular = Font(name="Segoe UI", size=10)
font_small = Font(name="Segoe UI", size=9)
font_small_italic = Font(name="Segoe UI", size=9, italic=True, color=GRAY_TEXT)

# Fills
fill_primary_header = PatternFill(start_color=DARK_GREEN, end_color=DARK_GREEN, fill_type="solid")
fill_sec_header = PatternFill(start_color=FOREST_GREEN, end_color=FOREST_GREEN, fill_type="solid")
fill_kpi = PatternFill(start_color=MINT_LIGHT, end_color=MINT_LIGHT, fill_type="solid")
fill_zebra = PatternFill(start_color="F9FBF9", end_color="F9FBF9", fill_type="solid")
fill_white = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")
fill_highlight = PatternFill(start_color="E3F2FD", end_color="E3F2FD", fill_type="solid")

# Borders
thin_gray = Side(border_style="thin", color=BORDER_GRAY)
thin_green = Side(border_style="thin", color=MINT_BORDER)
border_cell = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
border_kpi = Border(left=thin_green, right=thin_green, top=thin_green, bottom=thin_green)

# Alignments
align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")
align_wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_wrap_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

# ==============================================================================
# SHEET 1: PROJECT DASHBOARD
# ==============================================================================

# Row 1-2: Title Banner
ws_dash.merge_cells("A1:H1")
ws_dash["A1"] = "KhetSathi 360 — Project Executive Dashboard"
ws_dash["A1"].font = font_title
ws_dash["A1"].fill = fill_primary_header
ws_dash["A1"].alignment = align_center

ws_dash.merge_cells("A2:H2")
ws_dash["A2"] = "1M1B Green Internship – Youth Impact Realization Program (YIRP) | Owner: Vineet Shukla | Domain: Agriculture & Environment | Region: Uttar Pradesh"
ws_dash["A2"].font = font_subtitle
ws_dash["A2"].fill = fill_primary_header
ws_dash["A2"].alignment = align_center
ws_dash.row_dimensions[1].height = 28
ws_dash.row_dimensions[2].height = 20

# Row 3: Metadata bar
ws_dash["A3"] = "Internship Timeline:"
ws_dash["B3"] = "08-Nov-2026 to 30-Dec-2026"
ws_dash["C3"] = "Current Phase:"
ws_dash["D3"] = "Phase 4: Prototype Dev & Field Testing"
ws_dash["E3"] = "Mentor:"
ws_dash["F3"] = "Paramjeet (paramjeet@onemoneb.org)"
ws_dash["G3"] = "Report Date:"
ws_dash["H3"] = "=TODAY()"

for col in ["A", "C", "E", "G"]:
    ws_dash[f"{col}3"].font = font_bold
    ws_dash[f"{col}3"].fill = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")
    ws_dash[f"{col}3"].alignment = align_right
for col in ["B", "D", "F", "H"]:
    ws_dash[f"{col}3"].font = font_regular
    ws_dash[f"{col}3"].alignment = align_left
ws_dash["H3"].number_format = "YYYY-MM-DD"
ws_dash["H3"].alignment = align_center
ws_dash.row_dimensions[3].height = 22

# Row 5: KPI Summary Header
ws_dash.merge_cells("A5:H5")
ws_dash["A5"] = "REAL-TIME PROJECT PERFORMANCE INDICATORS (AUTOMATED FROM WORK TRACKER)"
ws_dash["A5"].font = font_sec_hdr
ws_dash["A5"].fill = fill_sec_header
ws_dash["A5"].alignment = align_center
ws_dash.row_dimensions[5].height = 22

# Row 6-7: 6 KPI Cards
# Card 1: Overall Progress (A6:A7) -> merged into A6:B6 and A7:B7
ws_dash.merge_cells("A6:B6")
ws_dash["A6"] = "OVERALL PROGRESS"
ws_dash["A6"].font = font_kpi_label
ws_dash["A6"].alignment = align_center
ws_dash["A6"].fill = fill_kpi

ws_dash.merge_cells("A7:B7")
ws_dash["A7"] = "=IFERROR(AVERAGE('WORK TRACKER'!H5:H50), 0)"
ws_dash["A7"].font = font_kpi_val
ws_dash["A7"].number_format = "0.0%"
ws_dash["A7"].alignment = align_center
ws_dash["A7"].fill = fill_kpi

# Card 2: Total Items (C6:C7)
ws_dash["C6"] = "TOTAL WORK ITEMS"
ws_dash["C6"].font = font_kpi_label
ws_dash["C6"].alignment = align_center
ws_dash["C6"].fill = fill_kpi

ws_dash["C7"] = "=COUNTA('WORK TRACKER'!A5:A50)"
ws_dash["C7"].font = font_kpi_val
ws_dash["C7"].alignment = align_center
ws_dash["C7"].fill = fill_kpi

# Card 3: Completed (D6:D7)
ws_dash["D6"] = "COMPLETED"
ws_dash["D6"].font = font_kpi_label
ws_dash["D6"].alignment = align_center
ws_dash["D6"].fill = fill_kpi

ws_dash["D7"] = '=COUNTIF(\'WORK TRACKER\'!G5:G50, "Completed")'
ws_dash["D7"].font = font_kpi_val
ws_dash["D7"].alignment = align_center
ws_dash["D7"].fill = fill_kpi

# Card 4: In Progress (E6:E7)
ws_dash["E6"] = "IN PROGRESS"
ws_dash["E6"].font = font_kpi_label
ws_dash["E6"].alignment = align_center
ws_dash["E6"].fill = fill_kpi

ws_dash["E7"] = '=COUNTIF(\'WORK TRACKER\'!G5:G50, "In Progress")'
ws_dash["E7"].font = font_kpi_val
ws_dash["E7"].alignment = align_center
ws_dash["E7"].fill = fill_kpi

# Card 5: Not Started (F6:F7)
ws_dash["F6"] = "UPCOMING / NOT STARTED"
ws_dash["F6"].font = font_kpi_label
ws_dash["F6"].alignment = align_center
ws_dash["F6"].fill = fill_kpi

ws_dash["F7"] = '=COUNTIF(\'WORK TRACKER\'!G5:G50, "Not Started")'
ws_dash["F7"].font = font_kpi_val
ws_dash["F7"].alignment = align_center
ws_dash["F7"].fill = fill_kpi

# Card 6: Overdue (G6:H6 merged, G7:H7 merged)
ws_dash.merge_cells("G6:H6")
ws_dash["G6"] = "OVERDUE ITEMS"
ws_dash["G6"].font = font_kpi_label
ws_dash["G6"].alignment = align_center
ws_dash["G6"].fill = fill_kpi

ws_dash.merge_cells("G7:H7")
ws_dash["G7"] = '=COUNTIFS(\'WORK TRACKER\'!I5:I50, "<"&TODAY(), \'WORK TRACKER\'!G5:G50, "<>Completed", \'WORK TRACKER\'!I5:I50, "<>")'
ws_dash["G7"].font = font_kpi_val
ws_dash["G7"].alignment = align_center
ws_dash["G7"].fill = fill_kpi

for r in [6, 7]:
    ws_dash.row_dimensions[r].height = 24
    for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        ws_dash[f"{col}{r}"].border = border_kpi

# Row 9: Phase Roadmap Section
ws_dash.merge_cells("A9:H9")
ws_dash["A9"] = "PROJECT ROADMAP & PHASE-WISE PROGRESSION"
ws_dash["A9"].font = font_sec_hdr
ws_dash["A9"].fill = fill_sec_header
ws_dash["A9"].alignment = align_center
ws_dash.row_dimensions[9].height = 22

headers_phase = ["Phase #", "Phase Name", "Primary Objective", "Timeline Window", "Deadline", "Status", "% Complete", "Key Deliverables"]
ws_dash.row_dimensions[10].height = 20
for c_idx, h in enumerate(headers_phase, start=1):
    cell = ws_dash.cell(row=10, column=c_idx, value=h)
    cell.font = font_tbl_hdr
    cell.fill = fill_sec_header
    cell.alignment = align_center
    cell.border = border_cell

phase_data = [
    ("Phase 1", "Problem Validation", "10-15 farmer interviews in UP, synthesize pain points in soil/weather/fertilizer", "08-Nov to 19-Nov-2026", "2026-11-19", "Completed", 1.0, "Farmer Survey Dataset & Problem Insights"),
    ("Phase 2", "Requirement Analysis & PRD", "Define MVP functional scope, farmer personas, and agronomic algorithm rules", "15-Nov to 21-Nov-2026", "2026-11-21", "Completed", 1.0, "PRD, Data Contracts & API Architecture Spec"),
    ("Phase 3", "Data Integration & Architecture", "Integrate 695 Indian district datasets, Open-Meteo live API, ICAR/FAO-56 engine", "18-Nov to 25-Nov-2026", "2026-11-24", "Completed", 1.0, "Clean Datasets (5646 rows) & FastAPI Backend"),
    ("Phase 4", "Prototype Development (Current)", "Build 2 functional prototypes: Farmer Advisory PWA & SHC Scanner / FPO Console", "24-Nov to 30-Nov-2026", "2026-11-30", "In Progress", 0.90, "Dual Functional Prototypes + 19/19 Unit Tests"),
    ("Phase 5", "Field Pilot & Farmer Testing", "Conduct field trials with 5+ farmers & SHGs in Ghazipur/UP; gather usability metrics", "01-Dec to 18-Dec-2026", "2026-12-18", "In Progress", 0.25, "Field Testing Report & Usability Scorecard"),
    ("Phase 6", "Final Reporting & Impact Showcase", "Deploy production release, assemble impact realization dossier and presentation", "19-Dec to 30-Dec-2026", "2026-12-30", "Not Started", 0.0, "Live Deployed Web App & 1M1B Final Report"),
]

for row_idx, p in enumerate(phase_data, start=11):
    ws_dash.row_dimensions[row_idx].height = 22
    for col_idx, val in enumerate(p, start=1):
        cell = ws_dash.cell(row=row_idx, column=col_idx, value=val)
        cell.font = font_regular
        cell.border = border_cell
        if col_idx in [1, 4, 5, 6]:
            cell.alignment = align_center
        elif col_idx == 7:
            cell.alignment = align_center
            cell.number_format = "0%"
        else:
            cell.alignment = align_wrap_left
        
        # Color coding status
        if col_idx == 6:
            if val == "Completed":
                cell.fill = PatternFill(start_color=STATUS_COMPLETED_FILL, end_color=STATUS_COMPLETED_FILL, fill_type="solid")
                cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_COMPLETED_TEXT)
            elif val == "In Progress":
                cell.fill = PatternFill(start_color=STATUS_IN_PROGRESS_FILL, end_color=STATUS_IN_PROGRESS_FILL, fill_type="solid")
                cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_IN_PROGRESS_TEXT)
            else:
                cell.fill = PatternFill(start_color=STATUS_PENDING_FILL, end_color=STATUS_PENDING_FILL, fill_type="solid")
                cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_PENDING_TEXT)

# Row 18: Prototype Highlights Section (Answers Mentor Feedback directly!)
ws_dash.merge_cells("A18:H18")
ws_dash["A18"] = "PROTOTYPE DELIVERABLES & TECHNICAL CAPABILITIES (BUILT WITH CURRENT RESOURCES)"
ws_dash["A18"].font = font_sec_hdr
ws_dash["A18"].fill = fill_sec_header
ws_dash["A18"].alignment = align_center
ws_dash.row_dimensions[18].height = 22

headers_proto = ["Module / Component", "User Persona", "Core Capabilities Delivered", "Tech Stack Used", "Spatial / Data Coverage", "Access / Verification", "Status", "Readiness"]
ws_dash.row_dimensions[19].height = 20
for c_idx, h in enumerate(headers_proto, start=1):
    cell = ws_dash.cell(row=19, column=c_idx, value=h)
    cell.font = font_tbl_hdr
    cell.fill = fill_sec_header
    cell.alignment = align_center
    cell.border = border_cell

proto_data = [
    ("Prototype 1: Farmer Advisory PWA", "Individual Smallholder Farmers", "Bilingual (Hindi/English), Voice Speech Narration, Auto GPS & Lat/Long input, ICAR/FAO-56 Irrigation Engine, Soil Card advisory", "HTML5 / Modern JS / Tailwind / Web Speech API", "Hyper-local GPS + 695 Indian Districts", "frontend/index.html (Port 8000)", "Completed", "Ready for Demo"),
    ("Prototype 2: SHC Scanner & FPO Console", "FPO Coordinators & Agri-Extension Agents", "Soil Health Card bulk upload & OCR simulation, NPK deficiency classification, batch farmer advisory generation", "Responsive Dashboard / ChartJS / CSV Export", "District / Village Aggregate Analytics", "frontend/fpo_dashboard.html", "Completed", "Ready for Demo"),
    ("Agronomic Core Engine & ML Residuals", "Engine & Decision Layer", "Hybrid ICAR/FAO-56 physical engine + Ridge residual layer trained on real data (5,646 samples), 59.6% MAE improvement", "Python 3.12 / scikit-learn / NumPy / Open-Meteo", "Pan-India Crop & Weather Coefficients", "app/baseline_engine.py & ml_pipeline/", "Completed", "Production Ready"),
    ("FastAPI REST Service & Verification Gates", "API & Integration Layer", "High-throughput endpoints (/api/v1/advisory, /api/v1/weather, /health), strict latency <50ms, 19/19 passing tests", "FastAPI / Uvicorn / Pydantic / Unittest", "Real-time Open-Meteo Weather API", "app/api.py & tests/test_system.py", "Completed", "100% Tests Green"),
]

for row_idx, p in enumerate(proto_data, start=20):
    ws_dash.row_dimensions[row_idx].height = 24
    for col_idx, val in enumerate(p, start=1):
        cell = ws_dash.cell(row=row_idx, column=col_idx, value=val)
        cell.font = font_regular
        cell.border = border_cell
        if col_idx in [2, 5, 6, 7, 8]:
            cell.alignment = align_center
        else:
            cell.alignment = align_wrap_left
        
        if col_idx in [7, 8]:
            cell.fill = PatternFill(start_color=STATUS_COMPLETED_FILL, end_color=STATUS_COMPLETED_FILL, fill_type="solid")
            cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_COMPLETED_TEXT)

# Row 25: Mentor Review & Action Response Log
ws_dash.merge_cells("A25:H25")
ws_dash["A25"] = "MENTOR FEEDBACK LOG & IMMEDIATE ACTIONS TAKEN"
ws_dash["A25"].font = font_sec_hdr
ws_dash["A25"].fill = fill_sec_header
ws_dash["A25"].alignment = align_center
ws_dash.row_dimensions[25].height = 22

headers_mentor = ["Review Date", "Mentor Name", "Trainer / Mentor Feedback", "Direct Action Taken by Vineet", "Impact / Deliverable Result", "Resolution Status", "Target Verification", "Notes"]
ws_dash.row_dimensions[26].height = 20
for c_idx, h in enumerate(headers_mentor, start=1):
    cell = ws_dash.cell(row=26, column=c_idx, value=h)
    cell.font = font_tbl_hdr
    cell.fill = fill_sec_header
    cell.alignment = align_center
    cell.border = border_cell

mentor_data = [
    ("2026-11-12", "Paramjeet (paramjeet@onemoneb.org)", "There are a lot of sheets in your tracker , make your tracker simpler with 1 or 2 sheets with real time updates", "Consolidated the 5 fragmented sheets into exactly 2 interconnected sheets: 1) Executive Dashboard with real-time dynamic KPI formulas, 2) Master Operational Work Tracker.", "Simplified navigation, single source of truth, automated live calculations.", "Resolved", "Immediate", "Trainer can review entire progress at a single glance without sheet hopping."),
    ("2026-11-19", "Paramjeet (paramjeet@onemoneb.org)", "Start your work with your current resources. Dont wait for other dependencies , start creating your prototype.", "Did not wait for physical sensors or external grants; leveraged local Python, FastAPI, and HTML5/JS to build both Prototype 1 (Farmer PWA) and Prototype 2 (FPO Console) immediately.", "Two production-ready prototypes built and verified with real open datasets & 19/19 passing test gates.", "Resolved", "Immediate", "Prototypes are fully interactive and ready for demonstration on localhost or cloud."),
    ("2026-11-26", "Paramjeet (paramjeet@onemoneb.org)", "Review technical architecture & public agri dataset integration", "Trained ML layer on 5,646 real samples across 695 Indian districts; linked Open-Meteo live weather forecasts to automate ET0 water requirement calculations.", "Real-world agronomic accuracy guaranteed with ±15% ICAR safety bounds.", "Completed", "26-Nov-2026", "Full architecture document and test logs available in repository."),
]

for row_idx, m in enumerate(mentor_data, start=27):
    ws_dash.row_dimensions[row_idx].height = 30
    for col_idx, val in enumerate(m, start=1):
        cell = ws_dash.cell(row=row_idx, column=col_idx, value=val)
        cell.font = font_regular
        cell.border = border_cell
        if col_idx in [1, 2, 6, 7]:
            cell.alignment = align_center
        else:
            cell.alignment = align_wrap_left
        if col_idx == 6:
            cell.fill = PatternFill(start_color=STATUS_COMPLETED_FILL, end_color=STATUS_COMPLETED_FILL, fill_type="solid")
            cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_COMPLETED_TEXT)

# Set Column Widths for Sheet 1
dash_col_widths = {
    "A": 16,
    "B": 24,
    "C": 34,
    "D": 24,
    "E": 20,
    "F": 22,
    "G": 16,
    "H": 26,
}
for col_letter, width in dash_col_widths.items():
    ws_dash.column_dimensions[col_letter].width = width


# ==============================================================================
# SHEET 2: WORK TRACKER
# ==============================================================================

# Row 1-2: Banner
ws_tracker.merge_cells("A1:K1")
ws_tracker["A1"] = "KhetSathi 360 — Master Work & Operational Tracker"
ws_tracker["A1"].font = font_title
ws_tracker["A1"].fill = fill_primary_header
ws_tracker["A1"].alignment = align_center

ws_tracker.merge_cells("A2:K2")
ws_tracker["A2"] = "Consolidated Operational Registry: Project Tasks, Field Research Observations, and Milestone Deliverables"
ws_tracker["A2"].font = font_subtitle
ws_tracker["A2"].fill = fill_primary_header
ws_tracker["A2"].alignment = align_center
ws_tracker.row_dimensions[1].height = 28
ws_tracker.row_dimensions[2].height = 20

# Row 4: Table Headers
tracker_headers = [
    "Task ID", "Phase / Module", "Category", "Task / Activity Description",
    "Deliverable Output & Technical Evidence", "Priority", "Status",
    "Progress %", "Target Due Date", "Actual Completion", "Trainer Notes / Alignment"
]
ws_tracker.row_dimensions[4].height = 24
for c_idx, h in enumerate(tracker_headers, start=1):
    cell = ws_tracker.cell(row=4, column=c_idx, value=h)
    cell.font = font_tbl_hdr
    cell.fill = fill_sec_header
    cell.alignment = align_center
    cell.border = border_cell

# Consolidated Work Items (Tasks + Research Observations + Prototype Milestones)
tasks_master = [
    ("TASK-001", "Phase 1: Validation", "Ideation", "Domain Selection & Problem Scoping in AgriTech", "Finalized KhetSathi 360 concept addressing smallholder resource mismanagement in UP", "High", "Completed", 1.0, "2026-11-08", "2026-11-08", "1M1B Domain Approved"),
    ("TASK-002", "Phase 1: Validation", "Research", "Literature & Policy Review (ICAR, PMKSY, Soil Health Scheme)", "Synthesized national agricultural schemes and identified digital advisory gaps", "High", "Completed", 1.0, "2026-11-12", "2026-11-11", "Aligned with national priorities"),
    ("TASK-003", "Phase 1: Validation", "Field Research", "Farmer Field Interviews & Empathy Mapping (10-15 farmers in UP)", "Synthesized 4 core field observations (OBS-01 to OBS-04: Soil degradation, NPK misuse, climate risk)", "High", "Completed", 1.0, "2026-11-19", "2026-11-15", "Validated real farmer pain points"),
    ("TASK-004", "Phase 2: Requirements", "Specification", "Product Requirements Document (PRD) & Data Contracts", "Defined MVP user stories, bilingual requirements, and data contract specifications (app/contracts.py)", "High", "Completed", 1.0, "2026-11-21", "2026-11-17", "Spec-driven development workflow"),
    ("TASK-005", "Phase 3: Data & Arch", "Engineering", "Agronomic Baseline Engine Development (FAO-56 & ICAR)", "Coded deterministic Penman-Monteith ET0 and crop coefficient engine (app/baseline_engine.py)", "High", "Completed", 1.0, "2026-11-23", "2026-11-18", "Preserves ICAR scientific validity"),
    ("TASK-006", "Phase 3: Data & Arch", "Data Science", "Real Agronomic Data Integration & Ridge Residual Model", "Integrated 5,646 real samples across 695 Indian districts; trained Ridge residual layer (59.6% MAE boost)", "High", "Completed", 1.0, "2026-11-25", "2026-11-22", "Zero synthetic data in training"),
    ("TASK-007", "Phase 4: Prototype", "Backend", "FastAPI REST API & Open-Meteo Live Forecast Integration", "Built endpoints (/api/v1/advisory, /weather), real-time weather sync, lat/long geolocation support", "High", "Completed", 1.0, "2026-11-27", "2026-11-24", "Sub-50ms p95 latency"),
    ("TASK-008", "Phase 4: Prototype", "Frontend", "Prototype 1: Farmer Advisory PWA with Speech Narration", "Built bilingual (Hindi/English) PWA with voice readout, GPS auto-location, interactive advice (frontend/index.html)", "High", "Completed", 1.0, "2026-11-29", "2026-11-25", "Addresses mentor advice: Started prototype immediately"),
    ("TASK-009", "Phase 4: Prototype", "Frontend", "Prototype 2: Soil Health Card Scanner & FPO Console", "Built extension officer / FPO portal for batch soil card analysis and village insights (frontend/fpo_dashboard.html)", "Medium", "Completed", 1.0, "2026-11-30", "2026-11-26", "Dual-prototype milestone met"),
    ("TASK-010", "Phase 4: Prototype", "Quality Assurance", "System Testing, Promotion Verification & WCAG 2.2 AA Audit", "Created 19/19 passing automated tests (tests/test_system.py); verified accessibility and screen readers", "High", "Completed", 1.0, "2026-11-30", "2026-11-28", "Production-grade reliability"),
    ("TASK-011", "Phase 5: Field Testing", "Field Validation", "Pilot Demonstrations with 5+ Farmers & SHG Leaders", "Conducting hands-on walkthroughs with UP farmers using live PWA and local soil card inputs", "High", "In Progress", 0.40, "2026-12-10", "", "Live testing in Ghazipur / Varanasi region"),
    ("TASK-012", "Phase 5: Field Testing", "Evaluation", "Farmer Feedback Synthesis & Usability Iteration", "Refining voice audio cues, font sizes, and vernacular terminology based on farmer feedback", "Medium", "In Progress", 0.20, "2026-12-18", "", "Continuous user-centric improvement"),
    ("TASK-013", "Phase 6: Deployment", "DevOps", "Production Cloud Deployment & Free Tier Hosting Setup", "Deploying FastAPI backend to Cloud Run / Render and PWA to GitHub Pages / Firebase Hosting", "High", "In Progress", 0.15, "2026-12-24", "", "Zero-cost student architecture"),
    ("TASK-014", "Phase 6: Deployment", "Reporting", "1M1B Final Internship Dossier & Video Walkthrough", "Drafting comprehensive project report, impact metrics, SDG-alignment, and pitch demonstration", "High", "Not Started", 0.0, "2026-12-30", "", "Final YIRP submission"),
    ("OBS-01", "Field Research", "Agronomy", "Soil Fertility Depletion & Imbalanced NPK Application", "Observation of urea overuse; incorporated soil pH and nutrient-balanced fertilizer recommendations", "High", "Completed", 1.0, "2026-11-15", "2026-11-15", "Built directly into recommendation logic"),
    ("OBS-02", "Field Research", "Agronomy", "Irrigation Inefficiencies & Groundwater Over-extraction", "Farmers irrigate on fixed schedules; implemented FAO-56 dynamic crop water demand calculation", "High", "Completed", 1.0, "2026-11-15", "2026-11-15", "Prevents 20-30% water wastage"),
]

for row_idx, task in enumerate(tasks_master, start=5):
    ws_tracker.row_dimensions[row_idx].height = 24
    is_zebra = (row_idx % 2 == 0)
    for col_idx, val in enumerate(task, start=1):
        cell = ws_tracker.cell(row=row_idx, column=col_idx, value=val)
        cell.font = font_regular
        cell.border = border_cell
        
        # Zebra striping for readability
        if is_zebra:
            cell.fill = fill_zebra
        
        # Alignments & formats
        if col_idx in [1, 2, 3, 6, 9, 10]:
            cell.alignment = align_center
        elif col_idx == 7:
            cell.alignment = align_center
            # Status colors
            if val == "Completed":
                cell.fill = PatternFill(start_color=STATUS_COMPLETED_FILL, end_color=STATUS_COMPLETED_FILL, fill_type="solid")
                cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_COMPLETED_TEXT)
            elif val == "In Progress":
                cell.fill = PatternFill(start_color=STATUS_IN_PROGRESS_FILL, end_color=STATUS_IN_PROGRESS_FILL, fill_type="solid")
                cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_IN_PROGRESS_TEXT)
            else:
                cell.fill = PatternFill(start_color=STATUS_PENDING_FILL, end_color=STATUS_PENDING_FILL, fill_type="solid")
                cell.font = Font(name="Segoe UI", size=10, bold=True, color=STATUS_PENDING_TEXT)
        elif col_idx == 8:
            cell.alignment = align_center
            cell.number_format = "0%"
        else:
            cell.alignment = align_wrap_left

# Set Column Widths for Sheet 2
tracker_col_widths = {
    "A": 12,
    "B": 20,
    "C": 15,
    "D": 32,
    "E": 44,
    "F": 12,
    "G": 14,
    "H": 13,
    "I": 15,
    "J": 17,
    "K": 32,
}
for col_letter, width in tracker_col_widths.items():
    ws_tracker.column_dimensions[col_letter].width = width

# Save Excel file
output_xlsx = "KhetSathi360_2Sheet_Tracker.xlsx"
wb.save(output_xlsx)
print(f"Workbook saved successfully as {output_xlsx}")
