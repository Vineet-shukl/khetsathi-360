// KhetSathi 360 TypeScript Contracts
// In 100% parity with app/contracts.py

export type CropId = 'wheat' | 'rice' | 'maize' | 'mustard' | 'gram' | 'sugarcane';
export type SoilTexture = 'clay_loam' | 'sandy_loam' | 'loam' | 'alluvial' | 'black';

export interface SoilTestInput {
  n_kg_ha?: number;
  p_kg_ha?: number;
  k_kg_ha?: number;
  oc_pct?: number;
  ph?: number;
  zn_ppm?: number;
  b_ppm?: number;
  fe_ppm?: number;
  s_ppm?: number;
}

export interface AdvisoryRequest {
  crop: CropId;
  variety?: string;
  area_ha: number;
  sowing_date?: string;
  irrigation_access?: boolean;
  irrigation_method?: 'tubewell' | 'canal' | 'rainfed';
  soil?: SoilTestInput;
  target_yield_t_ha?: number;
  lat?: number;
  lon?: number;
  language?: 'hi' | 'en';
}

export interface ProductPlan {
  dap_bags_50kg: number;
  urea_bags_45kg: number;
  mop_bags_50kg: number;
  zinc_sulphate_kg: number;
  timing: string;
  dap_nitrogen_credit_kg: number;
}

export interface IrrigationStage {
  stage_name: string;
  days_after_sowing: number;
  description: string;
  depth_mm: number;
}

export interface IrrigationSchedule {
  crop: string;
  growth_duration_days: number;
  kc_stages: number[];
  stages: IrrigationStage[];
  notes: string;
}

export interface WeatherIrregularity {
  code: string;
  severity: 'low' | 'moderate' | 'high' | 'critical';
  title_hi: string;
  title_en: string;
  desc_hi: string;
  desc_en: string;
  action_hi: string;
  action_en: string;
}

export interface WeatherForecastResponse {
  status: string;
  lat: number;
  lon: number;
  temp_c: number;
  relative_humidity_pct: number;
  et0_fao_mm_day: number;
  rain_prob_48h_pct: number;
  precipitation_sum_mm: number;
  wind_speed_kmh: number;
  weather_code: number;
  irregularities: WeatherIrregularity[];
  hold_urea_action: boolean;
}

export interface SatelliteVegetationIndex {
  source: string;
  ndvi: number;
  ndre: number;
  vegetation_vigor_status: string;
  soil_texture_profile: {
    clay_pct: number;
    sand_pct: number;
    bulk_density_g_cm3: number;
    cation_exchange_capacity_cmol_kg: number;
  };
  resolution_meters: number;
  satellite_constellation: string;
}

export interface OrganicInputPlan {
  crop: string;
  area_ha: number;
  vermicompost_tonnes: number;
  bio_npk_consortium_litres: number;
  jeevamrut_litres: number;
  neem_cake_kg: number;
  schedule_hi: string;
  schedule_en: string;
}

export interface OrganicEconomics {
  chemical_input_cost_inr: number;
  organic_input_cost_inr: number;
  input_savings_pct: number;
  expected_conventional_yield_kg_ha: number;
  expected_organic_yield_kg_ha: number;
  mandi_price_per_q_inr: number;
  organic_market_premium_pct: number;
  expected_organic_price_per_q_inr: number;
  conventional_gross_revenue_inr: number;
  organic_gross_revenue_inr: number;
  pkvy_annual_subsidy_inr: number;
  conventional_net_profit_inr: number;
  organic_net_profit_inr: number;
  profit_difference_inr: number;
}

export interface OrganicSupplierRoute {
  channel_name_hi: string;
  channel_name_en: string;
  description_hi: string;
  description_en: string;
  contact_url: string;
  badge: string;
}

export interface OrganicAdvisoryResponse {
  status: string;
  crop: string;
  area_ha: number;
  bio_inputs: OrganicInputPlan;
  economics: OrganicEconomics;
  supplier_routes: OrganicSupplierRoute[];
  motivation_summary_hi: string;
  motivation_summary_en: string;
}

export interface AdvisoryResponse {
  engine_version: string;
  confidence_mode: 'high_confidence' | 'baseline_estimate' | 'deterministic';
  hybrid_ml_active: boolean;
  npk_recommended_kg_ha: {
    n: number;
    p: number;
    k: number;
  };
  product_plan: ProductPlan;
  irrigation_schedule?: IrrigationSchedule;
  weather_context?: WeatherForecastResponse;
  satellite_vegetation?: SatelliteVegetationIndex;
  variety_recommended?: string;
  summary_hi?: string;
  summary_en?: string;
  hold_urea_advisory?: boolean;
}

export interface LocationSearchResult {
  display_name: string;
  district: string;
  state: string;
  lat: number;
  lon: number;
  confidence: number;
}
