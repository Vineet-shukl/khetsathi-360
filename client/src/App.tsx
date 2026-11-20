import React, { useCallback, useEffect, useRef, useState } from 'react';
import { fetchAdvisory, fetchOrganicAdvisory, fetchWeather, searchLocations } from './api/client';
import { AudioWaveformPlayer } from './components/AudioWaveformPlayer';
import { IrrigationTimeline } from './components/IrrigationTimeline';
import { OrganicEconomicsCard } from './components/OrganicEconomicsCard';
import { TactileBagCard } from './components/TactileBagCard';
import { WeatherAlertBanner } from './components/WeatherAlertBanner';
import type {
  AdvisoryResponse,
  CropId,
  LocationSearchResult,
  OrganicAdvisoryResponse,
  WeatherForecastResponse,
} from './types/contracts';

const CROPS: { id: CropId; icon: string; name_hi: string; name_en: string }[] = [
  { id: 'wheat', icon: '🌾', name_hi: 'गेहूं (Wheat)', name_en: 'Wheat' },
  { id: 'rice', icon: '🌱', name_hi: 'धान (Paddy/Rice)', name_en: 'Rice' },
  { id: 'maize', icon: '🌽', name_hi: 'मक्का (Maize)', name_en: 'Maize' },
  { id: 'mustard', icon: '🌼', name_hi: 'सरसों (Mustard)', name_en: 'Mustard' },
  { id: 'gram', icon: '🟤', name_hi: 'चना (Gram)', name_en: 'Gram' },
  { id: 'sugarcane', icon: '🎋', name_hi: 'गन्ना (Sugarcane)', name_en: 'Sugarcane' },
];

export const App: React.FC = () => {
  const [lang, setLang] = useState<'hi' | 'en'>('hi');
  const [selectedCrop, setSelectedCrop] = useState<CropId>('wheat');
  const [areaVal, setAreaVal] = useState<number>(1);
  const [areaUnit, setAreaUnit] = useState<'bigha_p' | 'bigha_k' | 'acre' | 'ha'>('ha');
  const [lat, setLat] = useState<number>(25.5928);
  const [lon, setLon] = useState<number>(83.577);
  const [locationName, setLocationName] = useState<string>('गाज़ीपुर, उत्तर प्रदेश (Ghazipur, UP)');

  // Pinpoint Location Autocomplete Search (Blinkit/Swiggy style)
  const [locQuery, setLocQuery] = useState<string>('');
  const [locSuggestions, setLocSuggestions] = useState<LocationSearchResult[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const searchTimeoutRef = useRef<number | null>(null);

  const [weather, setWeather] = useState<WeatherForecastResponse | undefined>();
  const [advisory, setAdvisory] = useState<AdvisoryResponse | undefined>();
  const [organic, setOrganic] = useState<OrganicAdvisoryResponse | undefined>();
  const [loading, setLoading] = useState<boolean>(false);
  const [isOffline, setIsOffline] = useState<boolean>(!navigator.onLine);

  const isHi = lang === 'hi';

  const areaHa = (() => {
    switch (areaUnit) {
      case 'bigha_p':
        return areaVal * 0.2529;
      case 'bigha_k':
        return areaVal * 0.1618;
      case 'acre':
        return areaVal * 0.4047;
      case 'ha':
      default:
        return areaVal;
    }
  })();

  const loadAdvisoryData = useCallback(async () => {
    setLoading(true);
    try {
      const [wData, advData, orgData] = await Promise.all([
        fetchWeather(lat, lon, lang).catch(() => undefined),
        fetchAdvisory({
          crop: selectedCrop,
          area_ha: areaHa,
          lat,
          lon,
          language: lang,
        }),
        fetchOrganicAdvisory(selectedCrop, areaHa).catch(() => undefined),
      ]);
      if (wData) setWeather(wData);
      setAdvisory(advData);
      if (orgData) setOrganic(orgData);
    } catch (err) {
      console.error('[KhetSathi] Failed to load advisory:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedCrop, areaHa, lang, lat, lon]);

  const triggerLocationSearch = (query: string) => {
    if (searchTimeoutRef.current) {
      window.clearTimeout(searchTimeoutRef.current);
    }
    if (!query || query.trim().length < 2) {
      setLocSuggestions([]);
      setShowSuggestions(false);
      return;
    }
    searchTimeoutRef.current = window.setTimeout(async () => {
      const results = await searchLocations(query);
      setLocSuggestions(results);
      setShowSuggestions(results.length > 0);
    }, 250);
  };

  useEffect(() => {
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  useEffect(() => {
    loadAdvisoryData();
  }, [loadAdvisoryData]);

  const currentCropObj = CROPS.find((c) => c.id === selectedCrop);
  const cropDisplayName = isHi ? currentCropObj?.name_hi || selectedCrop : currentCropObj?.name_en || selectedCrop;

  const dapCreditKg = advisory?.product_plan?.n_credit_from_dap_kg ?? advisory?.product_plan?.dap_nitrogen_credit_kg ?? 23.5;
  const audioText = advisory?.farmer_summary || advisory?.summary_hi || advisory?.summary_en || '';

  return (
    <div className="min-h-screen flex flex-col bg-[#f4f7f4] text-[#0f1f17]">
      {/* Top Header */}
      <header className="bg-[#0e2d1f] text-white sticky top-0 z-30 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-400/50 flex items-center justify-center text-xl">
              🌾
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base sm:text-lg font-bold">KhetSathi 360</span>
                <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                  {isHi ? 'प्रमाणित निर्णय प्रणाली' : 'Decision Engine'}
                </span>
              </div>
              <p className="text-xs text-emerald-100">
                {isHi ? 'मौसम व मिट्टी आधारित सटीक कृषि सलाह' : 'Soil & Weather Agronomy Engine'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            <a
              href="/legacy"
              className="text-xs font-semibold text-emerald-300 hover:text-white px-2 py-1 rounded border border-emerald-700 hover:border-emerald-500 transition hidden sm:inline-block"
              title={isHi ? 'क्लासिक तालिका दृश्य खोलें' : 'Open classic tabular view'}
            >
              📋 {isHi ? 'क्लासिक मोड' : 'Classic Mode'}
            </a>
            <button
              type="button"
              onClick={() => setLang(isHi ? 'en' : 'hi')}
              className="px-3 py-1.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 border border-white/20 text-white transition flex items-center gap-1 cursor-pointer"
            >
              <span>🌐</span> <span>{isHi ? 'हिन्दी / EN' : 'English / HI'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Offline Alert Banner */}
      {isOffline && (
        <aside className="bg-amber-500 text-amber-950 px-4 py-2 text-xs sm:text-sm font-bold text-center flex items-center justify-center gap-2 border-b border-amber-600 shadow-sm">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-950 animate-ping" />
          <span>
            {isHi
              ? '🌾 ऑफलाइन फील्ड मोड सक्रिय (Offline Mode) — स्थानीय मॉडल सक्रिय हैं।'
              : '🌾 Offline Field Mode Active — Operating using cached local agronomic models.'}
          </span>
        </aside>
      )}

      {/* Main Content */}
      <main className="max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 flex-1 space-y-6">
        {/* Step 1: Farm Location & Crop */}
        <section className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-slate-900">
                {isHi ? 'कदम 1: खेत का सटीक स्थान व फसल चयन' : 'Step 1: Farm Pinpoint Location & Crop Selection'}
              </h3>
              <p className="text-xs text-slate-500">
                📍 {locationName}
              </p>
            </div>
            <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 self-start sm:self-auto">
              {isHi ? 'ICAR पैकेज ऑफ प्रैक्टिसेज' : 'ICAR Package of Practices'}
            </span>
          </div>

          {/* Location Autocomplete (Blinkit/Swiggy style) */}
          <div className="relative">
            <label className="text-xs font-bold text-slate-700 block mb-1">
              {isHi ? 'गाँव / तहसील / ब्लॉक / जिला खोजें (सटीक मौसम व मिट्टी हेतु):' : 'Search Pinpoint Locality / Tehsil / Block / District:'}
            </label>
            <div className="relative flex items-center">
              <span className="absolute left-3 text-slate-400 text-sm">🔍</span>
              <input
                type="text"
                value={locQuery}
                onChange={(e) => {
                  setLocQuery(e.target.value);
                  triggerLocationSearch(e.target.value);
                }}
                onFocus={() => {
                  if (locSuggestions.length > 0) setShowSuggestions(true);
                }}
                placeholder={isHi ? 'उदा. Ghazipur, Karnal, Ludhiana, Varanasi...' : 'e.g. Ghazipur, Karnal, Ludhiana, Varanasi...'}
                className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            {/* Suggestions Dropdown */}
            {showSuggestions && locSuggestions.length > 0 && (
              <div className="absolute z-20 left-0 right-0 mt-1 bg-white border border-slate-200 rounded-xl shadow-lg max-h-56 overflow-y-auto divide-y divide-slate-100">
                {locSuggestions.map((item, idx) => {
                  const disp = item.name + (item.admin2 ? `, ${item.admin2}` : '') + (item.admin1 ? `, ${item.admin1}` : '');
                  return (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setLocationName(disp);
                        setLat(item.lat);
                        setLon(item.lon);
                        setLocQuery(disp);
                        setShowSuggestions(false);
                      }}
                      className="w-full text-left px-3 py-2.5 text-xs hover:bg-emerald-50 transition flex items-center justify-between cursor-pointer"
                    >
                      <div>
                        <span className="font-bold text-slate-800 block">{item.name}</span>
                        <span className="text-[10px] text-slate-500">
                          {item.admin2 ? `${item.admin2}, ` : ''}{item.admin1 || 'India'}
                        </span>
                      </div>
                      <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                        📍 {item.lat.toFixed(2)}, {item.lon.toFixed(2)}
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {loading && (
            <div className="text-xs text-emerald-800 font-bold bg-emerald-50/80 px-3 py-1.5 rounded-lg border border-emerald-200 inline-flex items-center gap-2 animate-pulse">
              <span>⏳</span> {isHi ? 'सटीक सलाह और मौसम डेटा लोड हो रहा है...' : 'Calculating scientific advisory and fetching microclimate data...'}
            </div>
          )}

          {/* Crop Chips */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700 block">
              {isHi ? 'फसल चुनें:' : 'Select Crop:'}
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
              {CROPS.map((crop) => {
                const active = crop.id === selectedCrop;
                return (
                  <button
                    key={crop.id}
                    type="button"
                    onClick={() => setSelectedCrop(crop.id)}
                    className={`p-3 rounded-xl border text-center transition flex flex-col items-center gap-1.5 cursor-pointer ${
                      active
                        ? 'border-emerald-600 bg-emerald-50 text-emerald-950 font-bold shadow-xs'
                        : 'border-slate-200 bg-white hover:bg-slate-50 text-slate-700'
                    }`}
                  >
                    <span className="text-2xl">{crop.icon}</span>
                    <span className="text-xs">
                      {isHi ? crop.name_hi : crop.name_en}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Farm Size & Units */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">
                {isHi ? 'खेत का क्षेत्रफल / रकबा:' : 'Farm Area / Size:'}
              </label>
              <input
                type="number"
                min="0.1"
                step="0.1"
                value={areaVal}
                onChange={(e) => setAreaVal(Math.max(0.1, parseFloat(e.target.value) || 1))}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-sm font-bold bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">
                {isHi ? 'इकाई (Unit):' : 'Unit:'}
              </label>
              <select
                value={areaUnit}
                onChange={(e) => setAreaUnit(e.target.value as any)}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-sm font-bold bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="bigha_p">बीघा / Pucca Bigha (≈ 0.25 Ha)</option>
                <option value="bigha_k">कच्चा बीघा / Kuccha Bigha (≈ 0.16 Ha)</option>
                <option value="acre">एकड़ / Acre (≈ 0.40 Ha)</option>
                <option value="ha">हेक्टेयर / Hectare (1.0 Ha)</option>
              </select>
            </div>
          </div>
        </section>

        {/* Step 2: Weather & Microclimate Safety Check */}
        {weather && (
          <section className="space-y-2">
            <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wide">
              {isHi ? 'कदम 2: आज का मौसम व सुरक्षा जांच' : 'Step 2: Weather & Microclimate Safety Check'}
            </h3>
            <WeatherAlertBanner weather={weather} isHi={isHi} />
          </section>
        )}

        {/* Step 3: Tactile Fertilizer Bags Plan */}
        {advisory && (
          <section className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  {isHi ? 'कदम 3: खेत में क्या करें (खाद की सटीक बोरियां)' : 'Step 3: What To Do in Your Field (Fertilizer Plan)'}
                </h3>
                <p className="text-xs text-slate-500">
                  {isHi
                    ? `रकबा: ${areaVal} ${areaUnit} (≈ ${areaHa.toFixed(2)} हे.) — ${cropDisplayName}`
                    : `Area: ${areaVal} ${areaUnit} (≈ ${areaHa.toFixed(2)} Ha) — ${cropDisplayName}`}
                </p>
              </div>

              {/* Neural TTS Voice Player */}
              {audioText && (
                <div className="w-full sm:w-80">
                  <AudioWaveformPlayer
                    text={audioText}
                    lang={lang}
                    isHi={isHi}
                  />
                </div>
              )}
            </div>

            {/* 3 Tactile Bags */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <TactileBagCard
                title={isHi ? 'बुवाई पर डीएपी (DAP 18-46-0)' : 'DAP (18-46-0) — Basal'}
                subtitle={isHi ? 'फास्फोरस व प्रारंभिक नाइट्रोजन' : 'Phosphorus & Starter N'}
                bags={advisory.product_plan?.dap_bags_50kg ?? 0}
                bagSizeKg={50}
                colorTheme="amber"
                icon="🌾"
                timingNote={
                  isHi
                    ? 'प्रयोग: बुवाई के समय बीज के नीचे 4-5 सेमी गहराई में दें।'
                    : 'Timing: Apply 4–5 cm below seed depth at sowing.'
                }
              />
              <TactileBagCard
                title={isHi ? 'यूरिया (Urea 46% N) — किश्तों में' : 'Urea (46% N) — Split Doses'}
                subtitle={isHi ? 'डीएपी की नाइट्रोजन काटकर शुद्ध' : 'Net Nitrogen after DAP credit'}
                bags={advisory.product_plan?.urea_bags_45kg ?? 0}
                bagSizeKg={45}
                colorTheme="emerald"
                icon="🧪"
                timingNote={
                  isHi
                    ? 'प्रयोग: पहली व दूसरी सिंचाई के बाद 2-3 किश्तों में दें।'
                    : 'Timing: Top-dress in 2–3 equal splits following irrigation.'
                }
                creditNote={
                  isHi
                    ? `डीएपी से मिली ${dapCreditKg.toFixed(1)} किलो नाइट्रोजन यूरिया में से घटा दी गई है।`
                    : `${dapCreditKg.toFixed(1)} kg N from DAP was deducted to avoid over-application.`
                }
              />
              <TactileBagCard
                title={isHi ? 'पोटाश (MOP 60% K₂O)' : 'Potash (MOP 60% K₂O)'}
                subtitle={isHi ? 'दाने का वजन, चमक व सूखा रक्षा' : 'Grain weight, shine & drought resistance'}
                bags={advisory.product_plan?.mop_bags_50kg ?? 0}
                bagSizeKg={50}
                colorTheme="blue"
                icon="💎"
                timingNote={
                  isHi
                    ? 'प्रयोग: बुवाई के समय डीएपी के साथ मिलाकर दें।'
                    : 'Timing: Apply as basal dressing with DAP at sowing.'
                }
              />
            </div>

            {/* Irrigation Schedule Timeline */}
            <IrrigationTimeline schedule={advisory.irrigation_schedule} isHi={isHi} />
          </section>
        )}

        {/* Organic Farming & Direct Supplier Engine */}
        {organic && (
          <section>
            <OrganicEconomicsCard
              organicData={organic}
              isHi={isHi}
              cropName={cropDisplayName}
              areaHa={areaHa}
            />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 mt-12 text-center text-xs text-slate-500 space-y-1">
        <p className="font-bold text-slate-700">
          KhetSathi 360 · National Digital Agri Decision Platform · Grounded in ICAR PoP, FAO-56 & DAC&FW Standards
        </p>
        <p>
          WCAG 2.2 Level AA Compliant · Bilingual Hindi / English · React 19 Client ·{' '}
          <a href="/legacy" className="underline text-emerald-700 hover:text-emerald-900">
            {isHi ? 'क्लासिक तालिका दृश्य' : 'Classic View'}
          </a>
        </p>
      </footer>
    </div>
  );
};

export default App;
