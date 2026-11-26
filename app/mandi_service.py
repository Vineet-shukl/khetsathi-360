"""
app/mandi_service.py — Real-Time Indian Mandi Price & CACP Benchmark Service.

Combines up to three verified data layers (in priority order):
  1. FPO Field Spot Quotes persisted in SQLite (instant coordinator updates)
  2. Live OGD Agmarknet daily mandi arrivals via api.data.gov.in (resource 9ef84268-d588-465a-a308-a864a43d0070)
     when DATA_GOV_IN_API_KEY is configured, cached for 15 minutes
  3. Official Government of India CACP 2025-26 / 2026-27 MSP/FRP benchmarks with regional APMC spread factors
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from app.contracts import CropId, MandiPricesResponse, MandiZoneQuote, ZoneId
from app.fpo_records_service import FPORecordsStore

logger = logging.getLogger(__name__)

AGMARKNET_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
MANDI_CACHE_TTL_SECONDS = 900.0  # 15 minutes
_AGMARKNET_CACHE: dict[str, tuple[float, dict[str, dict[str, Any]]]] = {}

# Current Official CACP / PIB Minimum Support Prices (2025-26 Kharif & 2026-27 Rabi / FRP)
CROP_PRICE_METADATA: dict[CropId, dict[str, Any]] = {
    "wheat": {
        "label_en": "Wheat",
        "label_hi": "गेहूं",
        "msp_inr_per_q": 2585.0,
        "season": "RMS 2026-27 CACP MSP",
        "agmarknet_commodity": "Wheat",
    },
    "rice": {
        "label_en": "Rice (Paddy Common)",
        "label_hi": "धान",
        "msp_inr_per_q": 2369.0,
        "season": "KMS 2025-26 CACP MSP",
        "agmarknet_commodity": "Paddy(Dhan)(Common)",
    },
    "maize": {
        "label_en": "Maize",
        "label_hi": "मक्का",
        "msp_inr_per_q": 2400.0,
        "season": "KMS 2025-26 CACP MSP",
        "agmarknet_commodity": "Maize",
    },
    "mustard": {
        "label_en": "Rapeseed & Mustard",
        "label_hi": "सरसों",
        "msp_inr_per_q": 6200.0,
        "season": "RMS 2026-27 CACP MSP",
        "agmarknet_commodity": "Mustard",
    },
    "gram": {
        "label_en": "Gram (Chana)",
        "label_hi": "चना",
        "msp_inr_per_q": 5875.0,
        "season": "RMS 2026-27 CACP MSP",
        "agmarknet_commodity": "Bengal Gram(Gram)(Whole)",
    },
    "sugarcane": {
        "label_en": "Sugarcane (FRP)",
        "label_hi": "गन्ना (FRP)",
        "msp_inr_per_q": 340.0,
        "season": "FRP Central Gov Benchmark",
        "agmarknet_commodity": "Sugarcane",
    },
}

ZONE_MARKET_HUBS: list[dict[str, Any]] = [
    {
        "zone": "zone4",
        "label": "Zone 4 · UP",
        "hub": "Ghazipur / Varanasi APMC",
        "state": "Uttar Pradesh",
        "min_f": 0.96,
        "modal_f": 1.03,
        "max_f": 1.09,
    },
    {
        "zone": "zone6",
        "label": "Zone 6 · PB/HR",
        "hub": "Khanna / Karnal Mandi",
        "state": "Punjab",
        "min_f": 0.99,
        "modal_f": 1.06,
        "max_f": 1.12,
    },
    {
        "zone": "zone8",
        "label": "Zone 8 · MP",
        "hub": "Sehore / Indore Mandi",
        "state": "Madhya Pradesh",
        "min_f": 0.94,
        "modal_f": 1.01,
        "max_f": 1.08,
    },
    {
        "zone": "zone9",
        "label": "Zone 9 · MH",
        "hub": "Nashik / Vashi APMC",
        "state": "Maharashtra",
        "min_f": 0.93,
        "modal_f": 0.99,
        "max_f": 1.06,
    },
    {
        "zone": "zone10",
        "label": "Zone 10 · KA",
        "hub": "Mandya / Hubli APMC",
        "state": "Karnataka",
        "min_f": 0.96,
        "modal_f": 1.02,
        "max_f": 1.09,
    },
    {
        "zone": "zone13",
        "label": "Zone 13 · GJ",
        "hub": "Anand / Unjha APMC",
        "state": "Gujarat",
        "min_f": 0.97,
        "modal_f": 1.04,
        "max_f": 1.11,
    },
]

_STATE_TO_ZONE: dict[str, ZoneId] = {
    **{h["state"].lower(): h["zone"] for h in ZONE_MARKET_HUBS},
    "bihar": "zone4",
    "haryana": "zone6",
    "rajasthan": "zone8",
    "telangana": "zone10",
    "andhra pradesh": "zone10",
}


def _format_market_name(rec: dict[str, Any], fallback_state: str) -> str:
    raw = str(rec.get("market") or rec.get("district") or fallback_state.title()).strip()
    lowered = raw.lower()
    if any(tok in lowered for tok in ("apmc", "mandi", "market", "samiti")):
        return raw
    return f"{raw} APMC"


def _fetch_agmarknet_records(commodity: str, force_refresh: bool = False) -> dict[str, dict[str, Any]]:
    """Fetch live Agmarknet prices by state if DATA_GOV_IN_API_KEY is configured."""
    api_key = (os.getenv("DATA_GOV_IN_API_KEY") or "").strip()
    if not api_key:
        return {}

    now_ts = time.time()
    cached = _AGMARKNET_CACHE.get(commodity)
    if cached and not force_refresh and (now_ts - cached[0]) < MANDI_CACHE_TTL_SECONDS:
        return cached[1]

    params = urllib.parse.urlencode(
        {
            "api-key": api_key,
            "format": "json",
            "limit": "300",
            "filters[commodity]": commodity,
        }
    )
    url = f"https://api.data.gov.in/resource/{AGMARKNET_RESOURCE_ID}?{params}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "KhetSathi360/2.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        records = payload.get("records", [])
        by_zone: dict[str, dict[str, Any]] = {}
        for rec in records:
            state = str(rec.get("state", "")).strip().lower()
            zone = _STATE_TO_ZONE.get(state)
            if not zone or zone in by_zone:
                continue
            try:
                modal_p = float(rec["modal_price"])
                if modal_p <= 0:
                    continue
                raw_min = float(rec.get("min_price") or modal_p)
                raw_max = float(rec.get("max_price") or modal_p)
            except (KeyError, TypeError, ValueError):
                continue
            min_p = raw_min if raw_min > 0 else modal_p
            max_p = raw_max if raw_max >= modal_p else modal_p
            by_zone[zone] = {
                "market_hub": _format_market_name(rec, state),
                "min_price_inr_per_q": round(min_p, 1),
                "modal_price_inr_per_q": round(modal_p, 1),
                "max_price_inr_per_q": round(max_p, 1),
                "arrival_date": str(rec.get("arrival_date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))),
            }
        _AGMARKNET_CACHE[commodity] = (now_ts, by_zone)
        return by_zone
    except Exception as exc:
        logger.warning("Agmarknet API fetch unavailable for %s: %s", commodity, exc)
        return {}


def get_live_mandi_prices(
    crop: CropId,
    store: FPORecordsStore,
    force_refresh: bool = False,
) -> MandiPricesResponse:
    """Return zone-wise mandi quotes merged from live Agmarknet, SQLite spot quotes, and CACP MSP."""
    meta = CROP_PRICE_METADATA[crop]
    msp = float(meta["msp_inr_per_q"])
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    live_api_by_zone = _fetch_agmarknet_records(meta["agmarknet_commodity"], force_refresh=force_refresh)
    fpo_quotes_by_zone = store.get_mandi_quotes_for_crop(crop)

    zones: list[MandiZoneQuote] = []
    live_hits = 0
    fpo_hits = 0

    for cfg in ZONE_MARKET_HUBS:
        z_id: ZoneId = cfg["zone"]
        if z_id in fpo_quotes_by_zone:
            q = fpo_quotes_by_zone[z_id]
            hub = str(q["market_hub"])
            min_p = float(q["min_price_inr_per_q"])
            modal_p = float(q["modal_price_inr_per_q"])
            max_p = float(q["max_price_inr_per_q"])
            arr_date = str(q["recorded_at"])[:10]
            arrivals = q.get("arrivals_tonnes")
            src = "fpo_spot_quote"
            fpo_hits += 1
        elif z_id in live_api_by_zone:
            q = live_api_by_zone[z_id]
            hub = str(q["market_hub"])
            min_p = float(q["min_price_inr_per_q"])
            modal_p = float(q["modal_price_inr_per_q"])
            max_p = float(q["max_price_inr_per_q"])
            arr_date = str(q["arrival_date"])
            arrivals = None
            src = "agmarknet_live"
            live_hits += 1
        else:
            hub = cfg["hub"]
            min_p = round(msp * cfg["min_f"])
            modal_p = round(msp * cfg["modal_f"])
            max_p = round(msp * cfg["max_f"])
            arr_date = today_str
            arrivals = None
            src = "cacp_apmc_benchmark"

        delta_inr = round(modal_p - msp, 1)
        delta_pct = round((delta_inr / max(1.0, msp)) * 100.0, 1)

        zones.append(
            MandiZoneQuote(
                zone=z_id,
                zone_label=cfg["label"],
                market_hub=hub,
                state=cfg["state"],
                min_price_inr_per_q=round(min_p, 1),
                modal_price_inr_per_q=round(modal_p, 1),
                max_price_inr_per_q=round(max_p, 1),
                msp_delta_inr_per_q=delta_inr,
                msp_delta_pct=delta_pct,
                price_source=src,
                arrival_date=arr_date,
                arrivals_tonnes=arrivals,
            )
        )

    cluster_modal = round(sum(z.modal_price_inr_per_q for z in zones) / max(1, len(zones)), 1)
    cluster_spread_pct = round(((cluster_modal - msp) / max(1.0, msp)) * 100.0, 1)

    if live_hits > 0 and fpo_hits > 0:
        primary_source = "Agmarknet Live + FPO Spot Quotes"
    elif live_hits > 0:
        primary_source = "Agmarknet Live (data.gov.in)"
    elif fpo_hits > 0:
        primary_source = "FPO Verified Spot Quote + CACP"
    else:
        primary_source = f"{meta['season']} + Regional APMC"

    return MandiPricesResponse(
        crop=crop,
        crop_label_en=meta["label_en"],
        crop_label_hi=meta["label_hi"],
        cacp_msp_inr_per_q=msp,
        cacp_msp_season=meta["season"],
        cluster_modal_price_inr_per_q=cluster_modal,
        cluster_msp_spread_pct=cluster_spread_pct,
        live_feed_connected=(live_hits > 0 or fpo_hits > 0),
        primary_source=primary_source,
        fetched_at_iso=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        zones=zones,
    )


def get_cluster_modal_price_map(store: FPORecordsStore) -> dict[CropId, float]:
    """Compute current live modal price per crop across all supported crops."""
    result: dict[CropId, float] = {}
    crop_ids: list[CropId] = ["wheat", "rice", "maize", "mustard", "gram", "sugarcane"]
    for cid in crop_ids:
        prices = get_live_mandi_prices(cid, store=store, force_refresh=False)
        result[cid] = prices.cluster_modal_price_inr_per_q
    return result
