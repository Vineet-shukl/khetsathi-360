// KhetSathi 360 TypeScript Contracts
// In 100% parity with app/contracts.py & defensive backward compatibility

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
  et0_mm_day?: number;
  rain_prob_48h_pct?: number;
}

export interface ProductPlan {
  dap_kg?: number;
  dap_bags_50kg: number;
  urea_kg?: number;
  urea_bags_45kg: number;
  mop_kg?: number;
  mop_bags_50kg: number;
  n_credit_from_dap_kg?: number;
  // Backward compatibility alias
  dap_nitrogen_credit_kg?: number;
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
  severity: string;
  title_en: string;
  title_hi: string;
  message_en: string;
  message_hi: string;
  action_en: string;
  action_hi: string;
  desc_en?: string;
  desc_hi?: string;
}

export interface WeatherForecastResponse {
  status: 'ok' | 'fallback';
  lat: number;
  lon: number;
  timezone: string;
  current_temp_c?: number;
  temp_c?: number; // alias
  relative_humidity_pct?: number;
  wind_speed_kmh?: number;
  weather_code: number;
  weather_condition: string;
  et0_fao_mm_day: number;
  rain_prob_48h_pct: number;
  precipitation_sum_mm: number;
  rain_guardrail_hold_urea: boolean;
  hold_urea_action?: boolean; // alias
  heat_stress_alert?: boolean;
  high_et0_alert?: boolean;
  high_humidity_alert?: boolean;
  irregularities: WeatherIrregularity[];
  source: string;
}

export interface SatelliteVegetationIndex {
  ndvi: number;
  ndre: number;
  crop_vigor_status: string;
  crop_vigor_status_hi: string;
  satellite_name?: string;
  resolution_meters?: number;
  soilgrids_clay_pct?: number;
  soilgrids_bulk_density_g_cm3?: number;
  soilgrids_cec_mmol_kg?: number;
  remote_sensing_action_en: string;
  remote_sensing_action_hi: string;
}

export interface OrganicInputPlan {
  vermicompost_tonnes: number;
  vermicompost_bags_50kg: number;
  bio_npk_consortia_litres: number;
  jeevamrut_litres: number;
  neem_cake_kg: number;
  neem_cake_bags_50kg: number;
  bio_control_agent: string;
  application_guidelines_hi: string[];
  application_guidelines_en: string[];
}

export interface OrganicEconomics {
  crop: CropId;
  area_ha: number;
  conventional_input_cost_inr: number;
  organic_input_cost_inr: number;
  input_cost_savings_inr: number;
  organic_market_premium_pct: number;
  expected_organic_price_per_q_inr: number;
  conventional_net_profit_inr: number;
  organic_net_profit_inr: number;
  net_profit_increase_inr: number;
  pkvy_annual_assistance_inr: number;
  total_farmer_benefit_inr: number;
}

export interface OrganicSupplierRoute {
  channel_name: string;
  channel_type: string;
  url: string;
  contact_info: string;
  benefit_description_hi: string;
  benefit_description_en: string;
  channel_name_hi?: string;
  channel_name_en?: string;
  description_hi?: string;
  description_en?: string;
  contact_url?: string;
}

export interface OrganicAdvisoryResponse {
  input_plan: OrganicInputPlan;
  bio_inputs?: OrganicInputPlan; // defensive alias
  economics: OrganicEconomics;
  supplier_routes: OrganicSupplierRoute[];
  conversion_timeline: string[];
  motivation_summary_hi?: string;
  motivation_summary_en?: string;
}

export interface AdvisoryResponse {
  model_version: string;
  serving_mode: string;
  confidence_mode: string;
  uncertainty_pct: number;
  rain_guardrail_hold_urea: boolean;
  recommended_variety: string;
  elemental_target_kg: Record<string, number>;
  ml_residual_delta_n_kg_ha: number;
  ml_confidence_band_kg_ha: number[];
  product_plan: ProductPlan;
  peak_etc_mm_day: number;
  soil_alerts: string[];
  farmer_summary: string;
  sources: string[];
  live_weather?: WeatherForecastResponse | null;
  satellite?: SatelliteVegetationIndex | null;
  summary_hi?: string;
  summary_en?: string;
  irrigation_schedule?: IrrigationSchedule;
}

export interface LocationSearchResult {
  name: string;
  admin1?: string | null; // State
  admin2?: string | null; // District
  lat: number;
  lon: number;
  country?: string;
  match_type?: string;
  display_name?: string;
  district?: string;
  state?: string;
}
