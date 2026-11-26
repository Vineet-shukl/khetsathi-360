from typing import Literal, Optional

from pydantic import BaseModel, Field

ZoneId = Literal["zone4", "zone6", "zone8", "zone9", "zone10", "zone13"]
CropId = Literal["wheat", "rice", "maize", "mustard", "gram", "sugarcane"]
IrrigationId = Literal["tubewell", "canal", "rainfed"]


class SoilTestInput(BaseModel):
    n_kg_ha: float | None = Field(default=None, ge=10.0, le=1000.0)
    p_kg_ha: float | None = Field(default=None, ge=1.0, le=150.0)
    k_kg_ha: float | None = Field(default=None, ge=10.0, le=1000.0)
    oc_pct: float | None = Field(default=None, ge=0.05, le=3.0)
    ph: float | None = Field(default=None, ge=3.5, le=10.0)
    zn_ppm: float | None = Field(default=None, ge=0.05, le=10.0)
    s_ppm: float | None = Field(default=None, ge=0.5, le=100.0)
    ec_dsm: float | None = Field(default=None, ge=0.05, le=15.0)


class AdvisoryRequest(BaseModel):
    zone: ZoneId = "zone4"
    crop: CropId = "wheat"
    area_ha: float = Field(default=1.0, ge=0.1, le=100.0)
    irrigation: IrrigationId = "tubewell"
    et0_mm_day: float = Field(default=3.8, ge=0.5, le=15.0)
    sowing_delay_days: int = Field(default=0, ge=0, le=45)
    rain_prob_48h_pct: int = Field(default=25, ge=0, le=100)
    lat: float | None = Field(default=None, ge=6.0, le=38.0)
    lon: float | None = Field(default=None, ge=68.0, le=98.0)
    soil: SoilTestInput | None = None
    language: Literal["en", "hi"] = "en"


class ProductPlan(BaseModel):
    dap_kg: float
    dap_bags_50kg: float
    urea_kg: float
    urea_bags_45kg: float
    mop_kg: float
    mop_bags_50kg: float
    n_credit_from_dap_kg: float


class SatelliteVegetationIndex(BaseModel):
    ndvi: float
    ndre: float
    crop_vigor_status: str
    crop_vigor_status_hi: str
    satellite_name: str = "Copernicus Sentinel-2 (ESA 10m MSI)"
    resolution_meters: float = 10.0
    soilgrids_clay_pct: float = 24.5
    soilgrids_bulk_density_g_cm3: float = 1.35
    soilgrids_cec_mmol_kg: float = 18.2
    remote_sensing_action_en: str
    remote_sensing_action_hi: str


class AdvisoryResponse(BaseModel):
    model_version: str
    serving_mode: Literal["hybrid_ml", "deterministic_fallback"]
    confidence_mode: Literal["shc_verified", "block_baseline_estimate"]
    uncertainty_pct: float
    rain_guardrail_hold_urea: bool
    recommended_variety: str
    elemental_target_kg: dict[str, float]
    ml_residual_delta_n_kg_ha: float
    ml_confidence_band_kg_ha: list[float]
    product_plan: ProductPlan
    peak_etc_mm_day: float
    soil_alerts: list[str]
    farmer_summary: str
    sources: list[str]
    live_weather: Optional["WeatherForecastResponse"] = None
    satellite: SatelliteVegetationIndex | None = None


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
    classifications: list[SHCClassification]
    amendment_flags: list[str]


class SHCOCRResponse(BaseModel):
    n_kg_ha: float
    p_kg_ha: float
    k_kg_ha: float
    oc_pct: float
    ph: float
    zn_ppm: float
    s_ppm: float = 12.0
    ec_dsm: float = 0.5
    district: str | None = None
    state: str | None = None
    confidence_pct: float = 95.0
    extracted_via: str = "gemini_vision"
    raw_summary: str | None = None


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
    admin1: str | None = None  # State
    admin2: str | None = None  # District
    lat: float
    lon: float
    country: str = "India"
    source: Literal["open_meteo_geocoding", "district_database"]
    display_name: str
    zone: str | None = None


class WeatherForecastResponse(BaseModel):
    status: Literal["ok", "fallback"]
    lat: float
    lon: float
    timezone: str
    current_temp_c: float | None = None
    relative_humidity_pct: float | None = None
    wind_speed_kmh: float | None = None
    weather_code: int = 0
    weather_condition: str
    et0_fao_mm_day: float
    rain_prob_48h_pct: int
    precipitation_sum_mm: float
    rain_guardrail_hold_urea: bool
    heat_stress_alert: bool = False
    high_et0_alert: bool = False
    high_humidity_alert: bool = False
    irregularities: list[WeatherIrregularity] = Field(default_factory=list)
    source: str


# ---------------------------------------------------------------------------
# Investor & Economic Decision Support Models
# ---------------------------------------------------------------------------
class YieldPredictionRequest(BaseModel):
    crop: CropId = "wheat"
    district_name: str | None = Field(default=None, description="Target district name, e.g. Ghazipur, Ludhiana")
    year: int = Field(default=2026, ge=1990, le=2030)
    area_ha: float = Field(default=1.0, ge=0.1, le=100.0)
    soil: SoilTestInput | None = None
    lat: float | None = Field(default=None, ge=6.0, le=38.0)
    lon: float | None = Field(default=None, ge=68.0, le=98.0)


class YieldPredictionResponse(BaseModel):
    crop: CropId
    district: str
    predicted_yield_t_ha: float
    confidence_interval_t_ha: list[float]
    historical_avg_yield_t_ha: float
    improvement_potential_pct: float
    model_version: str
    data_sources: list[str]


class ROIEstimateRequest(BaseModel):
    crop: CropId = "wheat"
    area_ha: float = Field(default=1.0, ge=0.1, le=100.0)
    current_yield_t_ha: float | None = Field(default=None, ge=0.1, le=200.0)
    district_name: str | None = None


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
    core_datasets: list[str]


class StateCoverageSummary(BaseModel):
    state: str
    zone: str
    districts_count: int
    representative_crops: list[str]


class AnalyticsCoverageResponse(BaseModel):
    total_districts: int
    total_states: int
    states: list[StateCoverageSummary]
    crops_supported: list[str]
    zones_covered: list[str]


class OrganicInputPlan(BaseModel):
    vermicompost_tonnes: float
    vermicompost_bags_50kg: float
    bio_npk_consortia_litres: float
    jeevamrut_litres: float
    neem_cake_kg: float
    neem_cake_bags_50kg: float
    bio_control_agent: str
    application_guidelines_hi: list[str]
    application_guidelines_en: list[str]


class OrganicEconomics(BaseModel):
    crop: CropId
    area_ha: float
    conventional_input_cost_inr: float
    organic_input_cost_inr: float
    input_cost_savings_inr: float
    organic_market_premium_pct: float
    expected_organic_price_per_q_inr: float
    conventional_net_profit_inr: float
    organic_net_profit_inr: float
    net_profit_increase_inr: float
    pkvy_annual_assistance_inr: float
    total_farmer_benefit_inr: float


class OrganicSupplierRoute(BaseModel):
    channel_name: str
    channel_type: Literal["Government Portal", "Buyer Network", "Certification System", "FPO Cluster"]
    url: str
    contact_info: str
    benefit_description_hi: str
    benefit_description_en: str


class OrganicAdvisoryResponse(BaseModel):
    input_plan: OrganicInputPlan
    economics: OrganicEconomics
    supplier_routes: list[OrganicSupplierRoute]
    conversion_timeline: list[str]


LotStatus = Literal["growing", "ready_to_sell", "dispatched"]
SoilRecordSource = Literal["verified_shc", "ocr_scan", "block_baseline"]


class MandiZoneQuote(BaseModel):
    zone: ZoneId
    zone_label: str
    market_hub: str
    state: str
    min_price_inr_per_q: float
    modal_price_inr_per_q: float
    max_price_inr_per_q: float
    msp_delta_inr_per_q: float
    msp_delta_pct: float
    price_source: Literal["agmarknet_live", "fpo_spot_quote", "cacp_apmc_benchmark"]
    arrival_date: str
    arrivals_tonnes: float | None = None


class MandiPricesResponse(BaseModel):
    crop: CropId
    crop_label_en: str
    crop_label_hi: str
    cacp_msp_inr_per_q: float
    cacp_msp_season: str
    cluster_modal_price_inr_per_q: float
    cluster_msp_spread_pct: float
    live_feed_connected: bool
    primary_source: str
    fetched_at_iso: str
    zones: list[MandiZoneQuote]


class MandiQuoteCreateRequest(BaseModel):
    crop: CropId
    zone: ZoneId = "zone4"
    market_hub: str = Field(..., min_length=2, max_length=80)
    min_price_inr_per_q: float = Field(..., ge=100.0, le=50000.0)
    modal_price_inr_per_q: float = Field(..., ge=100.0, le=50000.0)
    max_price_inr_per_q: float = Field(..., ge=100.0, le=50000.0)
    arrivals_tonnes: float | None = Field(default=None, ge=0.0, le=50000.0)


class FPOFarmerRecord(BaseModel):
    id: int
    farmer_name: str
    village: str
    district: str
    zone: ZoneId
    crop: CropId
    area_ha: float
    expected_quintals: float
    n_kg_ha: float
    p_kg_ha: float
    k_kg_ha: float
    oc_pct: float
    ph: float
    zn_ppm: float
    soil_source: SoilRecordSource
    lot_status: LotStatus
    live_modal_price_inr_per_q: float
    estimated_value_inr: float
    updated_at: str


class FPOFarmerRecordCreate(BaseModel):
    farmer_name: str = Field(..., min_length=2, max_length=80)
    village: str = Field(default="Cluster Member", min_length=1, max_length=80)
    district: str = Field(..., min_length=2, max_length=80)
    zone: ZoneId = "zone4"
    crop: CropId = "wheat"
    area_ha: float = Field(..., ge=0.05, le=200.0)
    expected_quintals: float | None = Field(default=None, ge=0.5, le=20000.0)
    n_kg_ha: float = Field(default=220.0, ge=10.0, le=1000.0)
    p_kg_ha: float = Field(default=14.0, ge=1.0, le=150.0)
    k_kg_ha: float = Field(default=170.0, ge=10.0, le=1000.0)
    oc_pct: float = Field(default=0.45, ge=0.05, le=3.0)
    ph: float = Field(default=7.2, ge=3.5, le=10.0)
    zn_ppm: float = Field(default=0.55, ge=0.05, le=10.0)
    soil_source: SoilRecordSource = "verified_shc"
    lot_status: LotStatus = "growing"


class FPOFarmerRecordUpdate(BaseModel):
    lot_status: LotStatus | None = None
    area_ha: float | None = Field(default=None, ge=0.05, le=200.0)
    expected_quintals: float | None = Field(default=None, ge=0.5, le=20000.0)
    soil_source: SoilRecordSource | None = None


class FPOLedgerSummary(BaseModel):
    total_records: int
    total_area_ha: float
    verified_shc_count: int
    ready_lots_count: int
    ready_quintals: float
    total_expected_quintals: float
    estimated_cluster_revenue_inr: float
    low_nitrogen_plots: int


class FPOLedgerResponse(BaseModel):
    summary: FPOLedgerSummary
    records: list[FPOFarmerRecord]
    synced_at_iso: str


class FPOAssimilationEventCreate(BaseModel):
    event_type: Literal["heavy_rain", "yellowing", "dry_spell"]
    note: str = Field(default="", max_length=240)
    district: str = Field(default="Cluster Plot", max_length=80)
    crop: CropId = "wheat"


class FPOAssimilationEvent(BaseModel):
    id: int
    event_type: Literal["heavy_rain", "yellowing", "dry_spell"]
    note: str
    district: str
    crop: CropId
    action_summary_en: str
    action_summary_hi: str
    created_at: str


AdvisoryResponse.model_rebuild()
