import React from 'react';
import type { OrganicAdvisoryResponse } from '../types/contracts';

interface OrganicEconomicsCardProps {
  organicData?: OrganicAdvisoryResponse;
  isHi: boolean;
  cropName: string;
  areaHa: number;
}

export const OrganicEconomicsCard: React.FC<OrganicEconomicsCardProps> = ({
  organicData,
  isHi,
  cropName,
  areaHa,
}) => {
  if (!organicData) return null;

  const { bio_inputs, economics, supplier_routes } = organicData;

  const handleWhatsAppConnect = () => {
    const text = isHi
      ? `🌾 *KhetSathi 360 — जैविक खेती व बाजार लिंकेज अनुरोध*\n\nफसल: ${cropName}\nरकबा: ${areaHa} हेक्टेयर\n\nमैं रासायनिक उर्वरक मुक्त जैविक खेती (PKVY/PGS प्रमाणीकरण) अपनाना चाहता हूँ। कृपया मुझे नजदीकी FPO एकत्रीकरण केंद्र व खरीद अनुबंध से जोड़ें।\n\nसत्यापित पोर्टल: https://www.jaivikkheti.in`
      : `🌾 *KhetSathi 360 — Organic Farming & Direct Market Linkage Request*\n\nCrop: ${cropName}\nArea: ${areaHa} Hectare\n\nI want to transition to certified organic cultivation under PKVY/PGS. Please connect me with the nearest FPO aggregation hub and direct buyer contract.\n\nVerified Portal: https://www.jaivikkheti.in`;
    window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`, '_blank');
  };

  return (
    <div className="p-5 rounded-2xl border-2 border-emerald-500 bg-gradient-to-br from-emerald-50/90 via-white to-amber-50/40 shadow-sm space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-emerald-200 pb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl" aria-hidden="true">
            🌿
          </span>
          <div>
            <h4 className="text-sm sm:text-base font-black text-emerald-950">
              {isHi
                ? 'जैविक खेती विकल्प एवं अधिक मुनाफा (Organic Farming & Profit Boost)'
                : 'Organic Farming Transition & Net Profit Boost'}
            </h4>
            <p className="text-[11px] text-emerald-800 font-semibold">
              {isHi
                ? 'रासायनिक खाद से 18% कम लागत, 25% अधिक बाजार मूल्य एवं ₹50,000 सरकारी अनुदान'
                : '18% lower input costs, 25% higher organic market premium, and ₹50,000 PKVY subsidy'}
            </p>
          </div>
        </div>
        <span className="inline-flex self-start sm:self-center text-[10px] font-black uppercase px-2.5 py-1 rounded-full bg-emerald-700 text-white shadow-xs">
          PKVY & PGS-India
        </span>
      </div>

      {/* Economics Profit Callout */}
      <div className="p-4 rounded-xl bg-emerald-900 text-white space-y-2">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <div>
            <span className="text-[11px] text-emerald-300 block font-bold">
              {isHi ? 'अनुमानित शुद्ध लाभ (Net Profit Comparison)' : 'Estimated Net Farmer Profit'}
            </span>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-black text-emerald-300">
                ₹{Math.round(economics.organic_net_profit_inr).toLocaleString('en-IN')}
              </span>
              <span className="text-xs text-slate-300 line-through">
                ₹{Math.round(economics.conventional_net_profit_inr).toLocaleString('en-IN')}
              </span>
            </div>
          </div>
          <div className="text-right">
            <span className="text-xs font-black text-amber-300 bg-amber-900/60 px-2 py-1 rounded border border-amber-600/50 block">
              +₹{Math.round(economics.net_profit_increase_inr).toLocaleString('en-IN')} {isHi ? 'अतिरिक्त लाभ' : 'Gain'}
            </span>
            <span className="text-[10px] text-emerald-200 font-medium">
              +{economics.organic_market_premium_pct}% {isHi ? 'ऑर्गेनिक मंडी प्रीमियम' : 'Premium'}
            </span>
          </div>
        </div>
        <p className="text-[11px] text-emerald-200/90 leading-relaxed border-t border-emerald-800 pt-2">
          💡 {isHi ? organicData.motivation_summary_hi : organicData.motivation_summary_en}
        </p>
      </div>

      {/* Bio-Fertilizer Package */}
      <div className="space-y-2">
        <h5 className="text-xs font-black text-emerald-950 uppercase tracking-wider flex items-center gap-1.5">
          <span>🧪</span> {isHi ? 'रासायनिक खाद के जैविक विकल्प (Bio-Input Package)' : 'Bio-Input Alternative Package'}
        </h5>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
          <div className="p-2.5 rounded-xl bg-white border border-emerald-300 shadow-2xs">
            <span className="text-[10px] font-bold text-slate-500 block">
              {isHi ? 'वर्मीकम्पोस्ट (DAP विकल्प)' : 'Vermicompost'}
            </span>
            <span className="font-black text-emerald-900 text-sm">
              {bio_inputs.vermicompost_tonnes.toFixed(1)} {isHi ? 'टन' : 'Tonnes'}
            </span>
          </div>
          <div className="p-2.5 rounded-xl bg-white border border-emerald-300 shadow-2xs">
            <span className="text-[10px] font-bold text-slate-500 block">
              {isHi ? 'तरल जैव-एनपीके (Urea विकल्प)' : 'Liquid Bio-NPK'}
            </span>
            <span className="font-black text-emerald-900 text-sm">
              {bio_inputs.liquid_bio_npk_litres.toFixed(1)} {isHi ? 'लीटर' : 'L'}
            </span>
          </div>
          <div className="p-2.5 rounded-xl bg-white border border-emerald-300 shadow-2xs">
            <span className="text-[10px] font-bold text-slate-500 block">
              {isHi ? 'देसी जीवामृत (सूक्ष्मजीव)' : 'Jeevamrut'}
            </span>
            <span className="font-black text-emerald-900 text-sm">
              {Math.round(bio_inputs.jeevamrut_litres)} {isHi ? 'लीटर' : 'L'}
            </span>
          </div>
          <div className="p-2.5 rounded-xl bg-white border border-emerald-300 shadow-2xs">
            <span className="text-[10px] font-bold text-slate-500 block">
              {isHi ? 'नीम खली (कीट रक्षा)' : 'Neem Cake'}
            </span>
            <span className="font-black text-emerald-900 text-sm">
              {Math.round(bio_inputs.neem_cake_kg)} {isHi ? 'किलो' : 'kg'}
            </span>
          </div>
        </div>
      </div>

      {/* Verified Supplier Routes */}
      <div className="space-y-2">
        <h5 className="text-xs font-black text-emerald-950 uppercase tracking-wider flex items-center gap-1.5">
          <span>🛒</span> {isHi ? 'सत्यापित सरकारी व खरीदार मार्ग' : 'Verified Direct Supplier & Buyer Routes'}
        </h5>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          {supplier_routes.map((route, i) => (
            <a
              key={i}
              href={route.contact_url}
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 rounded-xl border border-emerald-300 bg-white hover:bg-emerald-50 transition flex items-center justify-between group shadow-2xs cursor-pointer"
            >
              <div>
                <span className="font-bold text-emerald-950 group-hover:text-emerald-700 block">
                  {isHi ? route.channel_name_hi : route.channel_name_en}
                </span>
                <span className="text-[11px] text-slate-600 block">
                  {isHi ? route.description_hi : route.description_en}
                </span>
              </div>
              <span className="text-emerald-700 font-extrabold text-sm ml-2">↗</span>
            </a>
          ))}
        </div>
      </div>

      {/* 1-Click WhatsApp Direct Cluster & Buyer Connect */}
      <div className="p-3.5 rounded-xl bg-gradient-to-r from-emerald-100/90 to-teal-50 border border-emerald-300 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-2xs">
        <div className="flex items-center gap-2.5">
          <span className="text-2xl" aria-hidden="true">
            💬
          </span>
          <div>
            <span className="font-bold text-emerald-950 block text-xs sm:text-sm">
              {isHi ? 'जैविक समूह व FPO खरीदार संपर्क (WhatsApp Direct)' : 'Organic Cluster & FPO Buyer Connect'}
            </span>
            <span className="text-[11px] text-emerald-800 block">
              {isHi
                ? 'अपनी चयनित फसल व रकबे का विवरण सीधे जैविक क्लस्टर / FPO को साझा करें'
                : 'Share your crop and acreage details directly with regional organic buyers'}
            </span>
          </div>
        </div>
        <button
          type="button"
          onClick={handleWhatsAppConnect}
          className="w-full sm:w-auto px-4 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-extrabold text-xs rounded-xl shadow transition flex items-center justify-center gap-1.5 shrink-0 cursor-pointer"
        >
          <span>📲</span> <span>{isHi ? 'व्हाट्सएप पर संपर्क करें' : 'Connect via WhatsApp'}</span>
        </button>
      </div>
    </div>
  );
};
