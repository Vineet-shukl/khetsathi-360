"""
app/weather_service.py — Real-Time Weather, FAO-56 Evapotranspiration & Hyper-Local Pinpoint Location Service.

Fetches high-resolution numerical weather prediction (NWP) forecasts from Open-Meteo
for any latitude/longitude in India without requiring third-party API keys:
  - FAO-56 reference crop evapotranspiration (ET0) in mm/day
  - 48-hour precipitation probability (%) and rainfall accumulation (mm)
  - Current temperature, relative humidity, wind speed, and WMO weather condition
  - Automated 4-axis microclimate irregularity detection (rain, heat, ET0, humidity)
  - Hyper-local village, tehsil, and district geocoding search (country_code=IN)

Includes TTL caching (15 minutes) and graceful climatological fallback if offline.
"""
import logging
import time
import urllib.parse
import urllib.request
import json
from typing import Any, Dict, List, Optional, Tuple
from app.contracts import WeatherForecastResponse, WeatherIrregularity, LocationSearchResult

logger = logging.getLogger(__name__)

# In-memory TTL cache: (rounded_lat, rounded_lon, lang) -> (timestamp, WeatherForecastResponse)
_WEATHER_CACHE: Dict[Tuple[float, float, str], Tuple[float, WeatherForecastResponse]] = {}
CACHE_TTL_SECONDS = 900.0  # 15 minutes

# Geocoding cache: query_lower -> (timestamp, List[LocationSearchResult])
_GEOCODE_CACHE: Dict[str, Tuple[float, List[LocationSearchResult]]] = {}
GEOCODE_TTL_SECONDS = 1800.0  # 30 minutes

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


def evaluate_weather_irregularities(
    current_temp_c: Optional[float],
    relative_humidity_pct: Optional[float],
    et0_fao_mm_day: float,
    rain_prob_48h_pct: int,
    precipitation_sum_mm: float,
    language: str = "en",
) -> Tuple[bool, bool, bool, bool, List[WeatherIrregularity]]:
    """
    Evaluates 4 critical microclimatic irregularities and produces plain-language actionable advisories:
      1. Heavy Rain: rain_prob_48h > 60% or precip_sum >= 25mm -> Hold urea top-dressing.
      2. Heat Stress: temp >= 35°C -> Terminal heat warning, evening irrigation advised.
      3. High ET0 / Dry Deficit: ET0 >= 5.0 mm/d -> Soil moisture depletion, shorten irrigation cycle.
      4. High Humidity: RH >= 80% -> Fungal pathogen/pest incubation risk, moderate N and scout.
    """
    hold_urea = rain_prob_48h_pct > 60 or precipitation_sum_mm >= 25.0
    heat_stress = current_temp_c is not None and current_temp_c >= 35.0
    high_et0 = et0_fao_mm_day >= 5.0
    high_humidity = relative_humidity_pct is not None and relative_humidity_pct >= 80.0

    irregularities: List[WeatherIrregularity] = []

    if hold_urea:
        irregularities.append(
            WeatherIrregularity(
                code="heavy_rain",
                severity="alert",
                title_en="⚠️ Heavy Rain Warning — Hold Urea",
                title_hi="⚠️ भारी बारिश चेतावनी — यूरिया रोकें",
                message_en=f"Rain probability is {rain_prob_48h_pct}% with expected {precipitation_sum_mm:.1f} mm precipitation in the next 48 hours.",
                message_hi=f"अगले 48 घंटे में {rain_prob_48h_pct}% बारिश ({precipitation_sum_mm:.1f} मिमी) की संभावना है।",
                action_en="Do NOT broadcast Urea right now. Water will wash away nitrogen. Open field drainage channels to prevent waterlogging.",
                action_hi="अभी यूरिया का छिड़काव बिल्कुल न करें। पानी में बहने से खाद का भारी नुकसान होगा। खेत की जल निकासी नालियां खोल दें।",
            )
        )

    if heat_stress:
        irregularities.append(
            WeatherIrregularity(
                code="heat_stress",
                severity="warning",
                title_en="🌡️ High Temperature / Heat Stress Advisory",
                title_hi="🌡️ उच्च तापमान / लू (Heat Stress) चेतावनी",
                message_en=f"Current temperature is {current_temp_c:.1f}°C, which exceeds normal vegetative thresholds and accelerates transpiration.",
                message_hi=f"वर्तमान तापमान {current_temp_c:.1f}°C है, जिससे फसल में नमी की कमी व दाना सिकुड़ने का खतरा रहता है।",
                action_en="Apply light irrigation during early morning or late evening to buffer soil temperature and protect yield.",
                action_hi="सुबह या देर शाम के समय हल्की सिंचाई दें ताकि मिट्टी का तापमान नियंत्रित रहे और फसल को लू से बचाया जा सके।",
            )
        )

    if high_et0:
        irregularities.append(
            WeatherIrregularity(
                code="high_et0",
                severity="warning",
                title_en="☀️ High Evaporative Demand / Dry Spell",
                title_hi="☀️ तीव्र वाष्पीकरण व जल संकट चेतावनी",
                message_en=f"Daily water loss (ET0) is elevated at {et0_fao_mm_day:.2f} mm/day due to high solar radiation and wind.",
                message_hi=f"धूप व हवा के कारण मिट्टी से पानी खर्च (ET0) {et0_fao_mm_day:.2f} मिमी/दिन तक बढ़ गया है।",
                action_en="Advance your irrigation schedule by 2–3 days. Apply mulch or soil cover to conserve root-zone moisture.",
                action_hi="सिंचाई का समय 2-3 दिन पहले कर लें। नमी बनाए रखने के लिए पलवार (mulching) का उपयोग करें।",
            )
        )

    if high_humidity:
        irregularities.append(
            WeatherIrregularity(
                code="high_humidity",
                severity="info",
                title_en="💧 High Humidity — Disease & Pest Risk",
                title_hi="💧 अत्यधिक नमी — फफूंद व कीट जोखिम",
                message_en=f"Relative humidity is {relative_humidity_pct:.0f}%, creating favorable microclimate for fungal foliar diseases (rust, blast, blight).",
                message_hi=f"हवा में नमी {relative_humidity_pct:.0f}% है, जिससे पत्ती धब्बा, गेरुआ व झुलसा जैसे फफूंद रोगों का खतरा बढ़ जाता है।",
                action_en="Inspect crop canopy daily. Avoid excess nitrogen application and spray recommended biocontrol / fungicide if lesions appear.",
                action_hi="फसल की पत्तियों की नियमित जांच करें। अधिक यूरिया देने से बचें और लक्षण दिखने पर तुरंत अनुशंसित फफूंदनाशक का छिड़काव करें।",
            )
        )

    return hold_urea, heat_stress, high_et0, high_humidity, irregularities


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
        valid_probs = [p for p in rain_probs[:2] if p is not None]
        rain_prob_48h = int(max(valid_probs)) if valid_probs else 20

        rain_sums = daily.get("precipitation_sum", [0.0])
        precip_sum = round(float(sum(filter(None, rain_sums[:2]))), 1)

        hold_urea, heat_stress, high_et0, high_humidity, irregularities = evaluate_weather_irregularities(
            current_temp_c=current_temp,
            relative_humidity_pct=rh,
            et0_fao_mm_day=et0_val,
            rain_prob_48h_pct=rain_prob_48h,
            precipitation_sum_mm=precip_sum,
            language=language,
        )

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
            heat_stress_alert=heat_stress,
            high_et0_alert=high_et0,
            high_humidity_alert=high_humidity,
            irregularities=irregularities,
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
            heat_stress_alert=False,
            high_et0_alert=False,
            high_humidity_alert=False,
            irregularities=[],
            source="Climatological Baseline (Network Fallback)",
        )
        return fallback_resp


def search_pinpoint_locations(
    query: str,
    count: int = 8,
    district_records: Optional[List[Dict[str, Any]]] = None,
) -> List[LocationSearchResult]:
    """
    Searches villages, tehsils, mandis, towns, and districts across India (Blinkit/Swiggy style):
      1. Calls Open-Meteo Geocoding API with country_code=IN.
      2. Cross-references against 695 local district records.
      3. Merges and deduplicates coordinates.
    """
    q = query.strip()
    if not q or len(q) < 2:
        return []

    cache_key = q.lower()
    now = time.time()
    if cache_key in _GEOCODE_CACHE:
        cached_time, cached_results = _GEOCODE_CACHE[cache_key]
        if now - cached_time < GEOCODE_TTL_SECONDS:
            return cached_results

    results: List[LocationSearchResult] = []
    seen_coords = set()

    # 1. Search Open-Meteo Geocoding for hyper-local locality/village
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(q)}&count={count}&country_code=IN&language=en&format=json"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "KhetSathi360/2.0 (Agronomy-Engine; support@khetsathi.in)"},
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        for r in data.get("results", []):
            if r.get("country_code") != "IN" and r.get("country") != "India":
                continue
            name = r.get("name", "")
            admin1 = r.get("admin1")  # State
            admin2 = r.get("admin2")  # District / County
            lat = round(float(r.get("latitude")), 4)
            lon = round(float(r.get("longitude")), 4)

            coord_key = (round(lat, 2), round(lon, 2))
            if coord_key in seen_coords:
                continue
            seen_coords.add(coord_key)

            display_parts = [name]
            if admin2 and admin2 != name:
                display_parts.append(admin2)
            if admin1:
                display_parts.append(admin1)

            results.append(
                LocationSearchResult(
                    name=name,
                    admin1=admin1,
                    admin2=admin2,
                    lat=lat,
                    lon=lon,
                    country="India",
                    source="open_meteo_geocoding",
                    display_name=", ".join(display_parts),
                )
            )
    except Exception as exc:
        logger.debug("Open-Meteo geocoding search failed: %s", exc)

    # 2. Local District Catalog Fallback & Enrichment
    if district_records and len(results) < count:
        q_lower = q.lower()
        for rec in district_records:
            addr = rec.get("address", "")
            region = rec.get("region", "")
            if q_lower in addr.lower() or q_lower in region.lower():
                lat = round(float(rec.get("lat")), 4)
                lon = round(float(rec.get("lon")), 4)
                coord_key = (round(lat, 2), round(lon, 2))
                if coord_key in seen_coords:
                    continue
                seen_coords.add(coord_key)

                results.append(
                    LocationSearchResult(
                        name=addr,
                        admin1=region,
                        admin2=addr,
                        lat=lat,
                        lon=lon,
                        country="India",
                        source="district_database",
                        display_name=f"{addr}, {region}, India",
                    )
                )
                if len(results) >= count:
                    break

    _GEOCODE_CACHE[cache_key] = (now, results)
    return results
