from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field

ZoneId = Literal["zone4", "zone6", "zone8", "zone9", "zone10", "zone13"]
CropId = Literal["wheat", "rice", "maize", "mustard", "gram", "sugarcane"]
IrrigationId = Literal["tubewell", "canal", "rainfed"]


class SoilTestInput(BaseModel):
    n_kg_ha: Optional[float] = Field(default=None, ge=10.0, le=1000.0)
    p_kg_ha: Optional[float] = Field(default=None, ge=1.0, le=150.0)
    k_kg_ha: Optional[float] = Field(default=None, ge=10.0, le=1000.0)
    oc_pct: Optional[float] = Field(default=None, ge=0.05, le=3.0)
    ph: Optional[float] = Field(default=None, ge=3.5, le=10.0)
    zn_ppm: Optional[float] = Field(default=None, ge=0.05, le=10.0)
    s_ppm: Optional[float] = Field(default=None, ge=0.5, le=100.0)
    ec_dsm: Optional[float] = Field(default=None, ge=0.05, le=15.0)


class AdvisoryRequest(BaseModel):
    zone: ZoneId = "zone4"
    crop: CropId = "wheat"
    area_ha: float = Field(default=1.0, ge=0.1, le=100.0)
    irrigation: IrrigationId = "tubewell"
    et0_mm_day: float = Field(default=3.8, ge=0.5, le=15.0)
    sowing_delay_days: int = Field(default=0, ge=0, le=45)
    rain_prob_48h_pct: int = Field(default=25, ge=0, le=100)
    lat: Optional[float] = Field(default=None, ge=6.0, le=38.0)
    lon: Optional[float] = Field(default=None, ge=68.0, le=98.0)
    soil: Optional[SoilTestInput] = None
    language: Literal["en", "hi"] = "en"


class ProductPlan(BaseModel):
    dap_kg: float
    dap_bags_50kg: float
    urea_kg: float
    urea_bags_45kg: float
    mop_kg: float
    mop_bags_50kg: float
    n_credit_from_dap_kg: float


class AdvisoryResponse(BaseModel):
    model_version: str
    serving_mode: Literal["hybrid_ml", "deterministic_fallback"]
    confidence_mode: Literal["shc_verified", "block_baseline_estimate"]
    uncertainty_pct: float
    rain_guardrail_hold_urea: bool
    recommended_variety: str
    elemental_target_kg: Dict[str, float]
    ml_residual_delta_n_kg_ha: float
    ml_confidence_band_kg_ha: List[float]
    product_plan: ProductPlan
    peak_etc_mm_day: float
    soil_alerts: List[str]
    farmer_summary: str
    sources: List[str]
    live_weather: Optional["WeatherForecastResponse"] = None


class SHCParseRequest(BaseModel):
    n_kg_ha: float = Field(ge=0.0, le=1000.0)
    p_kg_ha: float = Field(ge=0.0, le=150.0)
    k_kg_ha: float = Field(ge=0.0, le=1000.0)
    oc_pct: float = Field(ge=0.0, le=3.0)
    ph: float = Field(ge=3.5, le=10.0)
    zn_ppm: float = Field(ge=0.0, le=10.0)
    s_ppm: float = Field(default=12.0, ge=0.0, le=100.0)
    ec_dsm: float = Field(default=0.5, ge=0.0, le=15.0)


class SHCClassification(BaseModel):
    parameter: str
    value: float
    unit: str
    status: str


class SHCParseResponse(BaseModel):
    classifications: List[SHCClassification]
    amendment_flags: List[str]


class WeatherIrregularity(BaseModel):
    code: Literal["heavy_rain", "heat_stress", "high_et0", "high_humidity"]
    severity: Literal["warning", "alert", "info"] = "warning"
    title_en: str
    title_hi: str
    message_en: str
    message_hi: str
    action_en: str
    action_hi: str


class LocationSearchResult(BaseModel):
    name: str
    admin1: Optional[str] = None  # State
    admin2: Optional[str] = None  # District
    lat: float
    lon: float
    country: str = "India"
    source: Literal["open_meteo_geocoding", "district_database"]
    display_name: str
    zone: Optional[str] = None


class WeatherForecastResponse(BaseModel):
    status: Literal["ok", "fallback"]
    lat: float
    lon: float
    timezone: str
    current_temp_c: Optional[float] = None
    relative_humidity_pct: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    weather_code: int = 0
    weather_condition: str
    et0_fao_mm_day: float
    rain_prob_48h_pct: int
    precipitation_sum_mm: float
    rain_guardrail_hold_urea: bool
    heat_stress_alert: bool = False
    high_et0_alert: bool = False
    high_humidity_alert: bool = False
    irregularities: List[WeatherIrregularity] = Field(default_factory=list)
    source: str


# ---------------------------------------------------------------------------
# Investor & Economic Decision Support Models
# ---------------------------------------------------------------------------
class YieldPredictionRequest(BaseModel):
    crop: CropId = "wheat"
    district_name: Optional[str] = Field(default=None, description="Target district name, e.g. Ghazipur, Ludhiana")
    year: int = Field(default=2026, ge=1990, le=2030)
    area_ha: float = Field(default=1.0, ge=0.1, le=100.0)
    soil: Optional[SoilTestInput] = None
    lat: Optional[float] = Field(default=None, ge=6.0, le=38.0)
    lon: Optional[float] = Field(default=None, ge=68.0, le=98.0)


class YieldPredictionResponse(BaseModel):
    crop: CropId
    district: str
    predicted_yield_t_ha: float
    confidence_interval_t_ha: List[float]
    historical_avg_yield_t_ha: float
    improvement_potential_pct: float
    model_version: str
    data_sources: List[str]


class ROIEstimateRequest(BaseModel):
    crop: CropId = "wheat"
    area_ha: float = Field(default=1.0, ge=0.1, le=100.0)
    current_yield_t_ha: Optional[float] = Field(default=None, ge=0.1, le=200.0)
    district_name: Optional[str] = None


class ROIEstimate(BaseModel):
    crop: CropId
    area_ha: float
    yield_t_ha: float
    production_tonnes: float
    msp_price_inr_per_q: float
    gross_revenue_inr: float
    total_input_cost_inr: float
    net_profit_inr: float
    roi_pct: float
    break_even_area_ha: float
    cost_benefit_ratio: float


class InvestorMetricsResponse(BaseModel):
    total_districts_covered: int
    total_data_points: int
    model_accuracy_mae: float
    model_improvement_pct: float
    avg_yield_improvement_pct: float
    unique_crops: int
    unique_states: int
    api_p95_latency_ms: float
    data_freshness: str
    safety_guardrails_enforced: str
    core_datasets: List[str]


class StateCoverageSummary(BaseModel):
    state: str
    zone: str
    districts_count: int
    representative_crops: List[str]


class AnalyticsCoverageResponse(BaseModel):
    total_districts: int
    total_states: int
    states: List[StateCoverageSummary]
    crops_supported: List[str]
    zones_covered: List[str]


AdvisoryResponse.model_rebuild()


