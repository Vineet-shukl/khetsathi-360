"""
app/weather_service.py — Real-Time Weather & FAO-56 Evapotranspiration Service.

Fetches high-resolution numerical weather prediction (NWP) forecasts from Open-Meteo
for any latitude/longitude in India without requiring third-party API keys:
  - FAO-56 reference crop evapotranspiration (ET0) in mm/day
  - 48-hour precipitation probability (%) and rainfall accumulation (mm)
  - Current temperature, relative humidity, wind speed, and WMO weather condition

Includes TTL caching (15 minutes) and graceful climatological fallback if offline.
"""
import logging
import time
import urllib.parse
import urllib.request
import json
from typing import Dict, Optional, Tuple
from app.contracts import WeatherForecastResponse

logger = logging.getLogger(__name__)

# In-memory TTL cache: (rounded_lat, rounded_lon, lang) -> (timestamp, WeatherForecastResponse)
_WEATHER_CACHE: Dict[Tuple[float, float, str], Tuple[float, WeatherForecastResponse]] = {}
CACHE_TTL_SECONDS = 900.0  # 15 minutes

# WMO Weather interpretation codes (WMO 4501)
WMO_CODE_MAP = {
    0: ("Clear sky", "साफ आसमान"),
    1: ("Mainly clear", "मुख्य रूप से साफ"),
    2: ("Partly cloudy", "आंशिक रूप से बादल"),
    3: ("Overcast", "घने बादल"),
    45: ("Fog", "कोहरा"),
    48: ("Depositing rime fog", "कोहरा"),
    51: ("Light drizzle", "हल्की बूंदाबांदी"),
    53: ("Moderate drizzle", "बूंदाबांदी"),
    55: ("Dense drizzle", "घनी बूंदाबांदी"),
    61: ("Slight rain", "हल्की बारिश"),
    63: ("Moderate rain", "मध्यम बारिश"),
    65: ("Heavy rain", "तेज़ बारिश"),
    71: ("Slight snow", "हल्की बर्फबारी"),
    73: ("Moderate snow", "बर्फबारी"),
    75: ("Heavy snow", "भारी बर्फबारी"),
    80: ("Slight rain showers", "हल्की बौछारें"),
    81: ("Moderate rain showers", "मध्यम बौछारें"),
    82: ("Violent rain showers", "तेज़ मूसलाधार बौछारें"),
    95: ("Thunderstorm", "गरज-चमक के साथ आंधी"),
    96: ("Thunderstorm with slight hail", "ओलावृष्टि के साथ आंधी"),
    99: ("Thunderstorm with heavy hail", "भारी ओलावृष्टि के साथ आंधी"),
}


def _get_wmo_description(code: int, lang: str = "en") -> str:
    en_desc, hi_desc = WMO_CODE_MAP.get(code, ("Variable conditions", "सामान्य मौसम"))
    return hi_desc if lang == "hi" else en_desc


def fetch_live_weather(
    lat: float,
    lon: float,
    timeout_s: float = 4.0,
    force_refresh: bool = False,
    language: str = "en",
) -> WeatherForecastResponse:
    """
    Fetch live weather and FAO-56 ET0 for given latitude and longitude.
    Falls back gracefully to climatological medians if offline or timed out.
    """
    cache_key = (round(lat, 2), round(lon, 2), language)
    now = time.time()

    if not force_refresh and cache_key in _WEATHER_CACHE:
        cached_time, cached_resp = _WEATHER_CACHE[cache_key]
        if now - cached_time < CACHE_TTL_SECONDS:
            return cached_resp

    params = {
        "latitude": f"{lat:.4f}",
        "longitude": f"{lon:.4f}",
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "et0_fao_evapotranspiration,precipitation_probability_max,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }
    url = f"https://api.open-meteo.com/v1/forecast?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "KhetSathi360/2.0 (Agronomy-Engine; support@khetsathi.in)"},
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        current = data.get("current", {})
        daily = data.get("daily", {})

        current_temp = current.get("temperature_2m")
        rh = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")
        w_code = current.get("weather_code", 0)

        et0_list = daily.get("et0_fao_evapotranspiration", [3.8])
        et0_val = round(float(et0_list[0]), 2) if et0_list and et0_list[0] is not None else 3.8

        rain_probs = daily.get("precipitation_probability_max", [20, 20])
        # Max rain probability across next 48 hours (today + tomorrow)
        valid_probs = [p for p in rain_probs[:2] if p is not None]
        rain_prob_48h = int(max(valid_probs)) if valid_probs else 20

        rain_sums = daily.get("precipitation_sum", [0.0])
        precip_sum = round(float(sum(filter(None, rain_sums[:2]))), 1)

        hold_urea = rain_prob_48h > 60

        condition_text = _get_wmo_description(w_code, lang=language)

        weather_resp = WeatherForecastResponse(
            status="ok",
            lat=round(lat, 4),
            lon=round(lon, 4),
            timezone=data.get("timezone", "Asia/Kolkata"),
            current_temp_c=round(current_temp, 1) if current_temp is not None else None,
            relative_humidity_pct=round(rh, 1) if rh is not None else None,
            wind_speed_kmh=round(wind_speed, 1) if wind_speed is not None else None,
            weather_code=w_code,
            weather_condition=condition_text,
            et0_fao_mm_day=et0_val,
            rain_prob_48h_pct=rain_prob_48h,
            precipitation_sum_mm=precip_sum,
            rain_guardrail_hold_urea=hold_urea,
            source="Open-Meteo High-Resolution NWP (Real-Time Live)",
        )
        _WEATHER_CACHE[cache_key] = (now, weather_resp)
        return weather_resp

    except Exception as exc:
        logger.warning(
            "Live weather fetch failed for lat=%.4f, lon=%.4f (%s); falling back to climatology",
            lat,
            lon,
            exc,
        )
        # Climatological baseline fallback: moderate ET0 (3.8 mm/d), 20% rain prob
        fallback_resp = WeatherForecastResponse(
            status="fallback",
            lat=round(lat, 4),
            lon=round(lon, 4),
            timezone="Asia/Kolkata",
            current_temp_c=27.0,
            relative_humidity_pct=55.0,
            wind_speed_kmh=8.0,
            weather_code=1,
            weather_condition=_get_wmo_description(1, lang=language),
            et0_fao_mm_day=3.8,
            rain_prob_48h_pct=20,
            precipitation_sum_mm=0.0,
            rain_guardrail_hold_urea=False,
            source="Climatological Baseline (Network Fallback)",
        )
        return fallback_resp
