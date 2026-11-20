import type {
  AdvisoryRequest,
  AdvisoryResponse,
  CropId,
  LocationSearchResult,
  OrganicAdvisoryResponse,
  SHCOCRResponse,
  SHCParseResponse,
  SoilTestInput,
  WeatherForecastResponse,
} from '../types/contracts';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function fetchAdvisory(req: AdvisoryRequest): Promise<AdvisoryResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/advisory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to fetch advisory' }));
    throw new Error(err.detail || 'Failed to fetch advisory');
  }
  return res.json();
}

export async function fetchOrganicAdvisory(
  crop: CropId,
  areaHa: number,
  conventionalProfit: number = 0
): Promise<OrganicAdvisoryResponse> {
  const url = `${BASE_URL}/api/v1/organic/advisory?crop=${encodeURIComponent(crop)}&area_ha=${areaHa}&conventional_profit=${conventionalProfit}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error('Failed to fetch organic advisory');
  }
  return res.json();
}

export async function searchLocations(query: string): Promise<LocationSearchResult[]> {
  if (!query || query.trim().length < 2) return [];
  try {
    const res = await fetch(`${BASE_URL}/api/v1/location/search?query=${encodeURIComponent(query.trim())}`);
    if (!res.ok) return [];
    const data = await res.json();
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.results)) return data.results;
    return [];
  } catch (err) {
    console.warn('[searchLocations] network error:', err);
    return [];
  }
}

export async function fetchWeather(lat: number, lon: number, lang: 'hi' | 'en' = 'hi'): Promise<WeatherForecastResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/weather?lat=${lat}&lon=${lon}&lang=${lang}`);
  if (!res.ok) {
    throw new Error('Failed to fetch weather forecast');
  }
  return res.json();
}

export async function uploadShcImage(file: File, district?: string): Promise<SHCOCRResponse> {
  const formData = new FormData();
  formData.append('file', file);
  const url = district
    ? `${BASE_URL}/api/v1/shc/ocr-upload?district=${encodeURIComponent(district)}`
    : `${BASE_URL}/api/v1/shc/ocr-upload`;
  const res = await fetch(url, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to extract Soil Health Card' }));
    throw new Error(err.detail || 'Failed to extract Soil Health Card');
  }
  return res.json();
}

export async function parseShc(soil: SoilTestInput): Promise<SHCParseResponse> {
  const payload = {
    n_kg_ha: soil.n_kg_ha ?? 240.0,
    p_kg_ha: soil.p_kg_ha ?? 14.5,
    k_kg_ha: soil.k_kg_ha ?? 185.0,
    oc_pct: soil.oc_pct ?? 0.45,
    ph: soil.ph ?? 7.4,
    zn_ppm: soil.zn_ppm ?? 0.65,
    s_ppm: soil.s_ppm ?? 12.0,
    ec_dsm: soil.ec_dsm ?? 0.5,
  };
  const res = await fetch(`${BASE_URL}/api/v1/shc/parse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error('Failed to parse Soil Health Card parameters');
  }
  return res.json();
}

export async function fetchDistrictBaseline(query?: string, lat?: number, lon?: number): Promise<any> {
  const params = new URLSearchParams();
  if (query) params.append('query', query);
  if (lat !== undefined && lon !== undefined) {
    params.append('lat', lat.toString());
    params.append('lon', lon.toString());
  }
  const res = await fetch(`${BASE_URL}/api/v1/district/baseline?${params.toString()}`);
  if (!res.ok) {
    throw new Error('Failed to fetch district soil baseline');
  }
  return res.json();
}

export function getTtsAudioUrl(text: string, lang: 'hi' | 'en' = 'hi'): string {
  return `${BASE_URL}/api/v1/tts/synthesize?text=${encodeURIComponent(text)}&lang=${lang}`;
}
