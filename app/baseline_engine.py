from typing import Dict, List, Tuple
from app.contracts import AdvisoryRequest, ProductPlan

ZONES: Dict[str, Dict] = {
    "zone4": {
        "name": "Middle Gangetic Plains (E. UP, Bihar)",
        "varieties": {"wheat": "HD-2967 / DBW-187", "rice": "MTU-7029 / Sahbhagi Dhan", "maize": "DHM-117", "mustard": "RH-749", "gram": "JG-14", "sugarcane": "Co-0238"},
        "baseline_soil": {"n": 240.0, "p": 15.0, "k": 180.0, "oc": 0.45, "ph": 7.2, "zn": 0.55},
    },
    "zone6": {
        "name": "Trans-Gangetic Plains (Punjab, Haryana)",
        "varieties": {"wheat": "PBW-826 / HD-3086", "rice": "PR-126 / Pusa Basmati 1121", "maize": "PMH-1", "mustard": "RH-725", "gram": "PBG-7", "sugarcane": "CoJ-85"},
        "baseline_soil": {"n": 290.0, "p": 22.0, "k": 195.0, "oc": 0.52, "ph": 7.6, "zn": 0.60},
    },
    "zone8": {
        "name": "Central Plateau & Hills (MP, Bundelkhand)",
        "varieties": {"wheat": "HI-1544 / MP-3336", "rice": "JR-201", "maize": "JM-216", "mustard": "Pusa Mustard-25", "gram": "JG-11 / RVG-202", "sugarcane": "CoJN-86572"},
        "baseline_soil": {"n": 215.0, "p": 13.0, "k": 230.0, "oc": 0.44, "ph": 7.4, "zn": 0.48},
    },
    "zone9": {
        "name": "Western Plateau & Hills (Vidarbha, MH)",
        "varieties": {"wheat": "NIAW-1994", "rice": "PKV-HMT", "maize": "Rajarshi", "mustard": "Shatabdi", "gram": "Jaki-9218", "sugarcane": "Co-86032"},
        "baseline_soil": {"n": 185.0, "p": 10.0, "k": 285.0, "oc": 0.39, "ph": 8.1, "zn": 0.42},
    },
    "zone10": {
        "name": "Southern Plateau & Hills (KA, AP, TN)",
        "varieties": {"wheat": "UAS-304", "rice": "BPT-5204 / RNR-15048", "maize": "NAH-1137", "mustard": "Local Check", "gram": "JG-11", "sugarcane": "Co-86032"},
        "baseline_soil": {"n": 225.0, "p": 16.0, "k": 210.0, "oc": 0.48, "ph": 7.0, "zn": 0.50},
    },
    "zone13": {
        "name": "Gujarat Plains & Hills (Gujarat)",
        "varieties": {"wheat": "GW-496", "rice": "GR-11", "maize": "GAYMH-1", "mustard": "GM-3", "gram": "GG-5", "sugarcane": "CoN-05071"},
        "baseline_soil": {"n": 205.0, "p": 14.0, "k": 240.0, "oc": 0.41, "ph": 7.7, "zn": 0.46},
    },
}

CROPS: Dict[str, Dict] = {
    "wheat":     {"n": 120.0, "p": 60.0, "k": 40.0, "kc_mid": 1.15},
    "rice":      {"n": 120.0, "p": 60.0, "k": 60.0, "kc_mid": 1.20},
    "maize":     {"n": 120.0, "p": 60.0, "k": 40.0, "kc_mid": 1.20},
    "mustard":   {"n": 80.0,  "p": 40.0, "k": 40.0, "kc_mid": 1.10},
    "gram":      {"n": 20.0,  "p": 40.0, "k": 20.0, "kc_mid": 1.05},
    "sugarcane": {"n": 250.0, "p": 85.0, "k": 85.0, "kc_mid": 1.25},
}


def resolve_soil(req: AdvisoryRequest) -> Tuple[Dict[str, float], bool]:
    base = ZONES[req.zone]["baseline_soil"]
    if req.soil is None or all(
        getattr(req.soil, f) is None for f in ("n_kg_ha", "p_kg_ha", "k_kg_ha")
    ):
        return dict(base), True

    resolved = {
        "n": req.soil.n_kg_ha if req.soil.n_kg_ha is not None else base["n"],
        "p": req.soil.p_kg_ha if req.soil.p_kg_ha is not None else base["p"],
        "k": req.soil.k_kg_ha if req.soil.k_kg_ha is not None else base["k"],
        "oc": req.soil.oc_pct if req.soil.oc_pct is not None else base["oc"],
        "ph": req.soil.ph if req.soil.ph is not None else base["ph"],
        "zn": req.soil.zn_ppm if req.soil.zn_ppm is not None else base["zn"],
    }
    return resolved, False


def compute_baseline_npk_ha(req: AdvisoryRequest, soil: Dict[str, float]) -> Tuple[float, float, float]:
    crop = CROPS[req.crop]
    n_mult = 1.05 if (soil["n"] < 280 and soil["oc"] < 0.5) else (0.75 if soil["n"] > 560 else (0.90 if soil["n"] >= 280 else 1.0))
    p_mult = 1.15 if soil["p"] < 10 else (0.75 if soil["p"] > 25 else 1.0)
    k_mult = 1.15 if soil["k"] < 120 else (0.70 if soil["k"] > 280 else 1.0)

    delay_factor = 0.92 if req.sowing_delay_days > 10 else 1.0
    rainfed_factor = 0.85 if req.irrigation == "rainfed" else 1.0

    req_n = crop["n"] * n_mult * delay_factor * rainfed_factor
    req_p = crop["p"] * p_mult * delay_factor * rainfed_factor
    req_k = crop["k"] * k_mult * delay_factor * rainfed_factor
    return req_n, req_p, req_k


def convert_to_bags(req_n_total: float, req_p_total: float, req_k_total: float) -> ProductPlan:
    dap_kg = req_p_total / 0.46
    n_credit = dap_kg * 0.18
    rem_n = max(0.0, req_n_total - n_credit)
    urea_kg = rem_n / 0.46
    mop_kg = req_k_total / 0.60

    return ProductPlan(
        dap_kg=round(dap_kg, 1),
        dap_bags_50kg=round((dap_kg / 50.0) * 2.0) / 2.0,
        urea_kg=round(urea_kg, 1),
        urea_bags_45kg=round((urea_kg / 45.0) * 2.0) / 2.0,
        mop_kg=round(mop_kg, 1),
        mop_bags_50kg=round((mop_kg / 50.0) * 2.0) / 2.0,
        n_credit_from_dap_kg=round(n_credit, 1),
    )


def evaluate_soil_alerts(soil: Dict[str, float]) -> List[str]:
    alerts: List[str] = []
    if soil["ph"] < 5.5:
        alerts.append(f"Acidic soil (pH {soil['ph']:.1f} < 5.5): apply agricultural lime before basal dose.")
    elif soil["ph"] > 8.5:
        alerts.append(f"Alkaline/sodic soil (pH {soil['ph']:.1f} > 8.5): apply gypsum with organic matter.")
    if soil["zn"] < 0.5:
        alerts.append(f"Zinc deficient ({soil['zn']:.2f} ppm < 0.50): add 25 kg/ha Zinc Sulphate (21%).")
    return alerts
