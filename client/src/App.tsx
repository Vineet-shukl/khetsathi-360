import React, { useCallback, useEffect, useRef, useState } from 'react';
import { fetchAdvisory, fetchOrganicAdvisory, fetchWeather, searchLocations } from './api/client';
import { AudioWaveformPlayer } from './components/AudioWaveformPlayer';
import { FarmerCommunityCard } from './components/FarmerCommunityCard';
import { IrrigationTimeline } from './components/IrrigationTimeline';
import { NavigationTabs, type TabId } from './components/NavigationTabs';
import { OrganicEconomicsCard } from './components/OrganicEconomicsCard';
import { PrintableSlip } from './components/PrintableSlip';
import { SatelliteCard } from './components/SatelliteCard';
import { ScientificConsole } from './components/ScientificConsole';
import { SoilCardLab } from './components/SoilCardLab';
import { TactileBagCard } from './components/TactileBagCard';
import { WeatherAlertBanner } from './components/WeatherAlertBanner';
import type {
  AdvisoryResponse,
  CropId,
  LocationSearchResult,
  OrganicAdvisoryResponse,
  SoilTestInput,
  WeatherForecastResponse,
} from './types/contracts';

const CROPS: { id: CropId; icon: string; name_hi: string; name_en: string; default_variety: string }[] = [
  { id: 'wheat', icon: '🌾', name_hi: 'गेहूं (Wheat)', name_en: 'Wheat', default_variety: 'HD-2967 / DBW-187' },
  { id: 'rice', icon: '🌱', name_hi: 'धान (Paddy/Rice)', name_en: 'Rice', default_variety: 'Pusa-1121 / Sarjoo-52' },
  { id: 'maize', icon: '🌽', name_hi: 'मक्का (Maize)', name_en: 'Maize', default_variety: 'Dekalb-9108 / PMH-1' },
  { id: 'mustard', icon: '🌼', name_hi: 'सरसों (Mustard)', name_en: 'Mustard', default_variety: 'Pusa Bold / Giriraj' },
  { id: 'gram', icon: '🟤', name_hi: 'चना (Gram)', name_en: 'Gram', default_variety: 'JG-14 / Radhey' },
  { id: 'sugarcane', icon: '🎋', name_hi: 'गन्ना (Sugarcane)', name_en: 'Sugarcane', default_variety: 'Co-0238 / Co-0118' },
];

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('advisory');
  const [lang, setLang] = useState<'hi' | 'en'>('hi');
  const [selectedCrop, setSelectedCrop] = useState<CropId>('wheat');
  const [areaVal, setAreaVal] = useState<number>(1);
  const [areaUnit, setAreaUnit] = useState<'bigha_p' | 'bigha_k' | 'acre' | 'ha'>('ha');
  const [lat, setLat] = useState<number>(25.5928);
  const [lon, setLon] = useState<number>(83.577);
  const [locationName, setLocationName] = useState<string>('गाज़ीपुर, उत्तर प्रदेश (Ghazipur, UP)');

  // Soil health parameters state (passed from SoilCardLab)
  const [soilInput, setSoilInput] = useState<SoilTestInput>({
    n_kg_ha: 220.0,
    p_kg_ha: 14.5,
    k_kg_ha: 180.0,
    oc_pct: 0.45,
    ph: 7.4,
    zn_ppm: 0.65,
  });

  // Pinpoint Location Autocomplete Search (Blinkit/Swiggy style)
  const [locQuery, setLocQuery] = useState<string>('');
  const [locSuggestions, setLocSuggestions] = useState<LocationSearchResult[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const [isDetectingGps, setIsDetectingGps] = useState<boolean>(false);
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
          soil: soilInput,
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
  }, [selectedCrop, areaHa, soilInput, lang, lat, lon]);

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

  const handleGpsDetect = () => {
    if (!navigator.geolocation) {
      alert(isHi ? 'आपके ब्राउज़र में जीपीएस सुविधा उपलब्ध नहीं है।' : 'Geolocation not supported by your browser.');
      return;
    }
    setIsDetectingGps(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const userLat = parseFloat(pos.coords.latitude.toFixed(4));
        const userLon = parseFloat(pos.coords.longitude.toFixed(4));
        setLat(userLat);
        setLon(userLon);
        const name = `${isHi ? 'खेत जीपीएस स्थान' : 'Farm GPS Location'} (${userLat}°N, ${userLon}°E)`;
        setLocationName(name);
        setLocQuery(name);
        setIsDetectingGps(false);
      },
      (err) => {
        console.warn('[GPS Detection] error:', err);
        alert(isHi ? 'जीपीएस स्थान प्राप्त नहीं हो सका। कृपया खोज बार में जिला या गाँव का नाम लिखें।' : 'Could not retrieve GPS location. Please search manually.');
        setIsDetectingGps(false);
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const handleShareOnWhatsApp = () => {
    if (!advisory) return;
    const plan = advisory.product_plan;
    const dapBags = (plan?.dap_bags_50kg ?? 0).toFixed(1);
    const ureaBags = (plan?.urea_bags_45kg ?? 0).toFixed(1);
    const mopBags = (plan?.mop_bags_50kg ?? 0).toFixed(1);

    const shareText = isHi
      ? `🌾 *KhetSathi 360 — किसान खाद सलाह पर्ची*\n\nस्थान: ${locationName}\nफसल: ${cropDisplayName}\nरकबा: ${areaVal} ${areaUnit} (≈ ${areaHa.toFixed(2)} हे.)\n\n*अनुशंसित खाद:*\n• डीएपी (DAP 50kg): *${dapBags} बोरी*\n• यूरिया (Urea 45kg): *${ureaBags} बोरी*\n• पोटाश (MOP 50kg): *${mopBags} बोरी*\n\n*मौसम अलर्ट:* ${weather?.current_temp_c ?? 25}°C, वर्षा संभावना: ${weather?.rain_prob_48h_pct ?? 0}%\n\nसत्यापित पोर्टल: https://khetsathi-360.onrender.com`
      : `🌾 *KhetSathi 360 — Farm Fertilizer Prescription*\n\nLocation: ${locationName}\nCrop: ${cropDisplayName}\nArea: ${areaVal} ${areaUnit} (≈ ${areaHa.toFixed(2)} Ha)\n\n*Prescription Bags:*\n• DAP (50kg): *${dapBags} Bags*\n• Urea (45kg): *${ureaBags} Bags*\n• MOP (50kg): *${mopBags} Bags*\n\nPortal: https://khetsathi-360.onrender.com`;

    window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}`, '_blank');
  };

  const handlePrintSlip = () => {
    window.print();
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
    <div className="min-h-screen flex flex-col bg-[#faf8f5] text-[#1a241e]">
      {/* Top Header - Claude Fable Aesthetic */}
      <header className="bg-[#143826] text-white sticky top-0 z-30 shadow-md no-print border-b border-[#0d2a1c]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-xl shadow-xs">
              🌾
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg sm:text-xl font-bold font-serif-fable tracking-tight">
                  KhetSathi 360
                </span>
                <span className="text-[10px] font-black uppercase px-2 py-0.5 rounded-full bg-[#c96442] text-white">
                  {isHi ? 'राष्ट्रीय डिजिटल कृषि' : 'National Agronomy'}
                </span>
              </div>
              <p className="text-[11px] text-emerald-100">
                {isHi ? 'सटीक मौसम व ICAR पैकेज ऑफ प्रैक्टिसेज आधारित निर्णय प्रणाली' : 'Precision Weather & ICAR Package of Practices Decision Engine'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            <a
              href="/legacy"
              className="text-xs font-semibold text-emerald-200 hover:text-white px-2.5 py-1.5 rounded-xl border border-emerald-700/80 hover:border-emerald-500 transition hidden md:inline-flex items-center gap-1.5"
              title={isHi ? 'क्लासिक तालिका दृश्य' : 'Classic View'}
            >
              <span>📋</span>
              <span>{isHi ? 'क्लासिक मोड' : 'Classic View'}</span>
            </a>

            <button
              type="button"
              onClick={() => setLang(isHi ? 'en' : 'hi')}
              aria-label={isHi ? 'Switch to English' : 'Switch to Hindi'}
              className="min-h-[44px] px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 border border-white/20 text-white transition flex items-center gap-1.5 cursor-pointer"
            >
              <span>🌐</span>
              <span>{isHi ? 'English' : 'हिन्दी'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Offline Alert Banner */}
      {isOffline && (
        <aside className="bg-amber-500 text-amber-950 px-4 py-2 text-xs sm:text-sm font-bold text-center flex items-center justify-center gap-2 border-b border-amber-600 shadow-sm no-print">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-950 animate-ping" />
          <span>
            {isHi
              ? '🌾 ऑफलाइन फील्ड मोड सक्रिय (Offline Mode) — स्थानीय मॉडल सक्रिय हैं।'
              : '🌾 Offline Field Mode Active — Operating using cached local agronomic models.'}
          </span>
        </aside>
      )}

      {/* Main Container */}
      <main className="max-w-7xl w-full mx-auto px-4 sm:px-6 py-5 flex-1 space-y-6">
        {/* Navigation Tabs (4 Modules) */}
        <section className="no-print">
          <NavigationTabs activeTab={activeTab} onTabChange={setActiveTab} isHi={isHi} />
        </section>

        {/* ============================================================== */}
        {/* TAB 1: KISAN SALAHKAR (ADVISORY SLIP)                           */}
        {/* ============================================================== */}
        {activeTab === 'advisory' && (
          <div className="space-y-6">
            {/* Step 1: Farm Location & Crop */}
            <section className="fable-card p-6 rounded-3xl space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#e6dfd3] pb-3">
                <div>
                  <h3 className="text-base sm:text-lg font-bold text-[#143826] font-serif-fable">
                    {isHi ? 'कदम 1: खेत का सटीक स्थान व फसल चयन' : 'Step 1: Farm Pinpoint Location & Crop Selection'}
                  </h3>
                  <p className="text-xs text-[#5f6b64]">
                    📍 {locationName}
                  </p>
                </div>
                <span className="text-xs font-bold text-emerald-900 bg-emerald-100 px-3 py-1 rounded-full border border-emerald-300 self-start sm:self-auto">
                  {isHi ? 'ICAR पैकेज ऑफ प्रैक्टिसेज' : 'ICAR Package of Practices'}
                </span>
              </div>

              {/* Pinpoint Location Search & GPS Button */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-[#143826] block">
                  {isHi ? 'गाँव / तहसील / ब्लॉक / जिला खोजें (सटीक मौसम व मिट्टी हेतु):' : 'Search Pinpoint Locality / Tehsil / Block / District:'}
                </label>

                <div className="flex flex-col sm:flex-row gap-2">
                  <div className="relative flex-1">
                    <span className="absolute left-3 top-3 text-slate-400 text-sm">🔍</span>
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
                      placeholder={isHi ? 'उदा. Ghazipur, Karnal, Ludhiana, Varanasi, Muzaffarnagar...' : 'e.g. Ghazipur, Karnal, Ludhiana, Varanasi, Muzaffarnagar...'}
                      className="w-full pl-9 pr-3 py-2.5 rounded-xl border border-[#e6dfd3] text-xs sm:text-sm bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600"
                    />

                    {/* Suggestions Dropdown */}
                    {showSuggestions && locSuggestions.length > 0 && (
                      <div className="absolute z-20 left-0 right-0 mt-1 bg-white border border-[#e6dfd3] rounded-2xl shadow-xl max-h-60 overflow-y-auto divide-y divide-slate-100">
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
                              className="w-full text-left px-3.5 py-2.5 text-xs hover:bg-emerald-50 transition flex items-center justify-between cursor-pointer"
                            >
                              <div>
                                <span className="font-bold text-slate-900 block">{item.name}</span>
                                <span className="text-[10px] text-slate-500">
                                  {item.admin2 ? `${item.admin2}, ` : ''}{item.admin1 || 'India'}
                                </span>
                              </div>
                              <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full">
                                📍 {item.lat.toFixed(2)}, {item.lon.toFixed(2)}
                              </span>
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>

                  {/* GPS Detector button */}
                  <button
                    type="button"
                    onClick={handleGpsDetect}
                    disabled={isDetectingGps}
                    className="min-h-[44px] px-4 py-2.5 rounded-xl bg-[#faf8f5] hover:bg-[#f4efe6] text-[#143826] font-bold text-xs border border-[#e6dfd3] transition flex items-center justify-center gap-1.5 cursor-pointer shrink-0"
                  >
                    <span>📍</span>
                    <span>{isDetectingGps ? (isHi ? 'जीपीएस खोज रहे हैं...' : 'Detecting GPS...') : (isHi ? 'मेरा स्थान (GPS)' : 'My Location (GPS)')}</span>
                  </button>
                </div>
              </div>

              {loading && (
                <div className="text-xs text-emerald-900 font-bold bg-emerald-50 px-3.5 py-2 rounded-xl border border-emerald-300 inline-flex items-center gap-2 animate-pulse">
                  <span>⏳</span>
                  <span>{isHi ? 'सटीक सलाह और मौसम डेटा लोड हो रहा है...' : 'Calculating scientific advisory and fetching microclimate data...'}</span>
                </div>
              )}

              {/* Crop Selector Chips */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-[#143826] block">
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
                        className={`min-h-[44px] p-3 rounded-2xl border text-center transition flex flex-col items-center gap-1.5 cursor-pointer select-none ${
                          active
                            ? 'border-[#143826] bg-[#143826] text-white font-bold shadow-md ring-2 ring-[#143826]'
                            : 'border-[#e6dfd3] bg-white hover:bg-[#faf8f5] text-slate-800'
                        }`}
                      >
                        <span className="text-2xl" aria-hidden="true">{crop.icon}</span>
                        <span className="text-xs leading-tight">
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
                  <label className="text-xs font-bold text-[#143826] block mb-1">
                    {isHi ? 'खेत का क्षेत्रफल / रकबा:' : 'Farm Area / Size:'}
                  </label>
                  <input
                    type="number"
                    min="0.1"
                    step="0.1"
                    value={areaVal}
                    onChange={(e) => setAreaVal(Math.max(0.1, parseFloat(e.target.value) || 1))}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-[#e6dfd3] text-sm font-bold bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600"
                  />
                </div>
                <div>
                  <label className="text-xs font-bold text-[#143826] block mb-1">
                    {isHi ? 'इकाई (Unit):' : 'Unit:'}
                  </label>
                  <select
                    value={areaUnit}
                    onChange={(e) => setAreaUnit(e.target.value as any)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-[#e6dfd3] text-sm font-bold bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600 cursor-pointer"
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
                <h3 className="text-sm font-bold text-[#143826] uppercase tracking-wide">
                  {isHi ? 'कदम 2: आज का मौसम व सुरक्षा जांच' : 'Step 2: Weather & Microclimate Safety Check'}
                </h3>
                <WeatherAlertBanner weather={weather} isHi={isHi} />
              </section>
            )}

            {/* Step 3: Tactile Fertilizer Bags Plan */}
            {advisory && (
              <section className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#e6dfd3] pb-3">
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-[#143826] font-serif-fable">
                      {isHi ? 'कदम 3: खेत में क्या करें (खाद की सटीक बोरियां)' : 'Step 3: What To Do in Your Field (Fertilizer Plan)'}
                    </h3>
                    <p className="text-xs text-[#5f6b64]">
                      {isHi
                        ? `रकबा: ${areaVal} ${areaUnit} (≈ ${areaHa.toFixed(2)} हे.) — ${cropDisplayName} (${advisory.recommended_variety || 'HD-2967'})`
                        : `Area: ${areaVal} ${areaUnit} (≈ ${areaHa.toFixed(2)} Ha) — ${cropDisplayName} (${advisory.recommended_variety || 'HD-2967'})`}
                    </p>
                  </div>

                  {/* Actions Bar (Neural TTS, Print Slip, WhatsApp) */}
                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      type="button"
                      onClick={handlePrintSlip}
                      className="min-h-[44px] px-3.5 py-2 bg-white hover:bg-slate-50 text-slate-800 font-bold text-xs rounded-xl border border-slate-300 transition flex items-center gap-1.5 shadow-2xs cursor-pointer"
                      title={isHi ? 'पर्ची प्रिंट करें या PDF सेव करें' : 'Print prescription slip'}
                    >
                      <span>🖨️</span>
                      <span>{isHi ? 'पर्ची प्रिंट' : 'Print Slip'}</span>
                    </button>

                    <button
                      type="button"
                      onClick={handleShareOnWhatsApp}
                      className="min-h-[44px] px-3.5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs rounded-xl transition flex items-center gap-1.5 shadow-2xs cursor-pointer"
                      title={isHi ? 'व्हाट्सएप पर शेयर करें' : 'Share on WhatsApp'}
                    >
                      <span>📲</span>
                      <span>{isHi ? 'व्हाट्सएप' : 'WhatsApp'}</span>
                    </button>
                  </div>
                </div>

                {/* Neural TTS Voice Player */}
                {audioText && (
                  <div className="w-full">
                    <AudioWaveformPlayer
                      text={audioText}
                      lang={lang}
                      isHi={isHi}
                    />
                  </div>
                )}

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

                {/* Satellite Remote Sensing Card */}
                <SatelliteCard satellite={advisory.satellite} isHi={isHi} />

                {/* Scientific Mode Accordion Console */}
                <ScientificConsole advisory={advisory} isHi={isHi} />
              </section>
            )}
          </div>
        )}

        {/* ============================================================== */}
        {/* TAB 2: SOIL HEALTH CARD LAB & MULTIMODAL OCR                   */}
        {/* ============================================================== */}
        {activeTab === 'soil_card' && (
          <SoilCardLab
            currentSoil={soilInput}
            onApplySoil={(newSoil) => {
              setSoilInput(newSoil);
              setActiveTab('advisory');
            }}
            isHi={isHi}
            district={locationName.split(',')[0]}
          />
        )}

        {/* ============================================================== */}
        {/* TAB 3: ORGANIC FARMING & SUBSIDIES                             */}
        {/* ============================================================== */}
        {activeTab === 'organic' && organic && (
          <OrganicEconomicsCard
            organicData={organic}
            isHi={isHi}
            cropName={cropDisplayName}
            areaHa={areaHa}
          />
        )}

        {/* ============================================================== */}
        {/* TAB 4: CONNECT WITH LOCAL FARMERS                              */}
        {/* ============================================================== */}
        {activeTab === 'community' && (
          <FarmerCommunityCard
            locationName={locationName}
            isHi={isHi}
            cropName={cropDisplayName}
          />
        )}

        {/* Printable Slip for Physical Prescription Print */}
        {advisory && (
          <PrintableSlip
            advisory={advisory}
            locationName={locationName}
            cropName={cropDisplayName}
            areaVal={areaVal}
            areaUnit={areaUnit}
            areaHa={areaHa}
            isHi={isHi}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-[#e6dfd3] py-6 mt-12 text-center text-xs text-[#5f6b64] space-y-1 no-print">
        <p className="font-bold text-[#143826]">
          KhetSathi 360 · National Digital Agri Decision Platform · Grounded in ICAR PoP, FAO-56 & DAC&FW Standards
        </p>
        <p>
          WCAG 2.2 Level AA Compliant · Bilingual Hindi / English · Claude Fable 5.2 Aesthetic ·{' '}
          <a href="/legacy" className="underline text-emerald-800 hover:text-emerald-950 font-semibold">
            {isHi ? 'क्लासिक तालिका दृश्य (/legacy)' : 'Classic View (/legacy)'}
          </a>
        </p>
      </footer>
    </div>
  );
};

export default App;
