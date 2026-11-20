import type {
  AdvisoryRequest,
  AdvisoryResponse,
  CropId,
  LocationSearchResult,
  OrganicAdvisoryResponse,
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
  const res = await fetch(`${BASE_URL}/api/v1/location/search?query=${encodeURIComponent(query.trim())}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.results || [];
}

export async function fetchWeather(lat: number, lon: number, lang: 'hi' | 'en' = 'hi'): Promise<WeatherForecastResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/weather?lat=${lat}&lon=${lon}&lang=${lang}`);
  if (!res.ok) {
    throw new Error('Failed to fetch weather forecast');
  }
  return res.json();
}

export function getTtsAudioUrl(text: string, lang: 'hi' | 'en' = 'hi'): string {
  return `${BASE_URL}/api/v1/tts/synthesize?text=${encodeURIComponent(text)}&lang=${lang}`;
}
