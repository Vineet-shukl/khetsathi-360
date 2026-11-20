import React, { useCallback, useEffect, useState } from 'react';
import { fetchAdvisory, fetchOrganicAdvisory, fetchWeather } from './api/client';
import { AudioWaveformPlayer } from './components/AudioWaveformPlayer';
import { IrrigationTimeline } from './components/IrrigationTimeline';
import { OrganicEconomicsCard } from './components/OrganicEconomicsCard';
import { TactileBagCard } from './components/TactileBagCard';
import { WeatherAlertBanner } from './components/WeatherAlertBanner';
import type {
  AdvisoryResponse,
  CropId,
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
  const [lat] = useState<number>(25.5928);
  const [lon] = useState<number>(83.577);
  const [locationName] = useState<string>('गाज़ीपुर, उत्तर प्रदेश (Ghazipur, UP)');

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
      console.error('Failed to load advisory:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedCrop, areaHa, lang, lat, lon]);

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

          <button
            type="button"
            onClick={() => setLang(isHi ? 'en' : 'hi')}
            className="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 border border-white/20 text-white transition flex items-center gap-1 cursor-pointer"
          >
            <span>🌐</span> <span>{isHi ? 'हिन्दी / EN' : 'English / HI'}</span>
          </button>
        </div>
      </header>

      {/* Offline Alert Banner */}
      {isOffline && (
        <aside className="bg-amber-500 text-amber-950 px-4 py-2 text-xs sm:text-sm font-bold text-center flex items-center justify-center gap-2 border-b border-amber-600 shadow-sm">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-950 animate-ping" />
          <span>
            {isHi
              ? '🌾 ऑफलाइन फील्ड मोड सक्रिय (Offline Mode) — कैश्ड डेटा व स्थानीय मॉडल सक्रिय हैं।'
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
                {isHi ? 'कदम 1: खेत का स्थान व फसल चयन' : 'Step 1: Farm Location & Crop Selection'}
              </h3>
              <p className="text-xs text-slate-500">
                📍 {locationName}
              </p>
            </div>
            <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
              {isHi ? 'ICAR पैकेज ऑफ प्रैक्टिसेज' : 'ICAR Package of Practices'}
            </span>
          </div>

          {loading && (
            <div className="text-xs text-emerald-800 font-bold bg-emerald-50/80 px-3 py-1.5 rounded-lg border border-emerald-200 inline-flex items-center gap-2 animate-pulse">
              <span>⏳</span>
              <span>{isHi ? 'सलाह की गणना जारी है...' : 'Calculating agronomic advisory...'}</span>
            </div>
          )}

          {/* Crop Selector Chips */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700 block">
              {isHi ? 'फसल चुनें (Select Target Crop):' : 'Select Target Crop:'}
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
              {CROPS.map((c) => {
                const active = selectedCrop === c.id;
                return (
                  <button
                    key={c.id}
                    type="button"
                    onClick={() => setSelectedCrop(c.id)}
                    className={`p-3 rounded-xl border text-xs font-bold flex flex-col items-center gap-1.5 transition cursor-pointer ${
                      active
                        ? 'border-emerald-600 bg-emerald-50 text-emerald-950 shadow-xs ring-2 ring-emerald-500'
                        : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <span className="text-2xl">{c.icon}</span>
                    <span>{isHi ? c.name_hi : c.name_en}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Area & Unit Selector */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">
                {isHi ? 'खेत का रकबा (Land Size Number):' : 'Land Area:'}
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
              <div className="w-full sm:w-80">
                <AudioWaveformPlayer
                  text={isHi ? advisory.summary_hi || '' : advisory.summary_en || ''}
                  lang={lang}
                  isHi={isHi}
                />
              </div>
            </div>

            {/* 3 Tactile Bags */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <TactileBagCard
                title={isHi ? 'बुवाई पर डीएपी (DAP 18-46-0)' : 'DAP (18-46-0) — Basal'}
                subtitle={isHi ? 'फास्फोरस व प्रारंभिक नाइट्रोजन' : 'Phosphorus & Starter N'}
                bags={advisory.product_plan.dap_bags_50kg}
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
                bags={advisory.product_plan.urea_bags_45kg}
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
                    ? `डीएपी से मिली ${advisory.product_plan.dap_nitrogen_credit_kg.toFixed(1)} किलो नाइट्रोजन यूरिया में से घटा दी गई है।`
                    : `${advisory.product_plan.dap_nitrogen_credit_kg.toFixed(1)} kg N from DAP was deducted to avoid over-application.`
                }
              />
              <TactileBagCard
                title={isHi ? 'पोटाश (MOP 60% K₂O)' : 'Potash (MOP 60% K₂O)'}
                subtitle={isHi ? 'दाने का वजन, चमक व सूखा रक्षा' : 'Grain weight, shine & drought resistance'}
                bags={advisory.product_plan.mop_bags_50kg}
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
        <p>WCAG 2.2 Level AA Compliant · Bilingual Hindi / English · React 19 Client</p>
      </footer>
    </div>
  );
};

export default App;
