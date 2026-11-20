import React from 'react';
import type { AdvisoryResponse } from '../types/contracts';

interface PrintableSlipProps {
  advisory: AdvisoryResponse;
  locationName: string;
  cropName: string;
  areaVal: number;
  areaUnit: string;
  areaHa: number;
  isHi: boolean;
}

export const PrintableSlip: React.FC<PrintableSlipProps> = ({
  advisory,
  locationName,
  cropName,
  areaVal,
  areaUnit,
  areaHa,
  isHi,
}) => {
  const plan = advisory.product_plan;
  const dapBags = plan?.dap_bags_50kg ?? 0;
  const ureaBags = plan?.urea_bags_45kg ?? 0;
  const mopBags = plan?.mop_bags_50kg ?? 0;
  const dapCredit = plan?.n_credit_from_dap_kg ?? plan?.dap_nitrogen_credit_kg ?? 23.5;

  const todayStr = new Date().toLocaleDateString(isHi ? 'hi-IN' : 'en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });

  return (
    <div className="hidden print:block p-8 font-sans bg-white text-black max-w-3xl mx-auto border border-black">
      {/* Header */}
      <div className="border-b-2 border-black pb-4 text-center space-y-1">
        <h1 className="text-2xl font-black tracking-tight">
          KhetSathi 360 · राष्ट्रीय डिजिटल कृषि निर्णय प्रणाली
        </h1>
        <p className="text-sm font-semibold">
          प्रमाणित किसान उर्वरक सलाह पर्ची (Certified Farm Prescription Slip)
        </p>
        <p className="text-xs text-gray-600">
          ICAR पैकेज ऑफ प्रैक्टिसेज, DAC&FW व FAO-56 मानकों पर आधारित
        </p>
      </div>

      {/* Farm details meta */}
      <div className="grid grid-cols-2 gap-4 py-4 border-b border-gray-400 text-xs">
        <div>
          <p><span className="font-bold">खेत का स्थान / Location:</span> {locationName}</p>
          <p><span className="font-bold">चयनित फसल / Crop:</span> {cropName}</p>
          <p><span className="font-bold">अनुशंसित किस्म / Variety:</span> {advisory.recommended_variety || 'HD-2967 / DBW-187'}</p>
        </div>
        <div>
          <p><span className="font-bold">पर्ची दिनांक / Date:</span> {todayStr}</p>
          <p><span className="font-bold">रकबा / Area:</span> {areaVal} {areaUnit} (≈ {areaHa.toFixed(2)} हेक्टेयर)</p>
          <p><span className="font-bold">मॉडल संस्करण / Version:</span> {advisory.model_version}</p>
        </div>
      </div>

      {/* Prescription Table */}
      <div className="py-4 space-y-3">
        <h3 className="text-sm font-black uppercase tracking-wide">
          1. खाद की सटीक बोरियां (Prescription Fertilizer Bags)
        </h3>
        <table className="w-full text-xs border-collapse border border-black">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-black p-2 text-left">उर्वरक (Fertilizer)</th>
              <th className="border border-black p-2 text-center">बोरी मात्रा (Bags)</th>
              <th className="border border-black p-2 text-center">कुल वजन (Kg)</th>
              <th className="border border-black p-2 text-left">प्रयोग की विधि व समय (Application Timing)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-black p-2 font-bold">डीएपी (DAP 18-46-0)</td>
              <td className="border border-black p-2 text-center font-black text-sm">{dapBags.toFixed(1)} बोरी (50kg)</td>
              <td className="border border-black p-2 text-center">{Math.round(dapBags * 50)} किग्रा</td>
              <td className="border border-black p-2">बुवाई के समय बीज के नीचे 4-5 सेमी गहराई में दें।</td>
            </tr>
            <tr>
              <td className="border border-black p-2 font-bold">यूरिया (Urea 46% N)</td>
              <td className="border border-black p-2 text-center font-black text-sm">{ureaBags.toFixed(1)} बोरी (45kg)</td>
              <td className="border border-black p-2 text-center">{Math.round(ureaBags * 45)} किग्रा</td>
              <td className="border border-black p-2">
                पहली व दूसरी सिंचाई के बाद 2-3 बराबर किश्तों में दें।<br />
                *(डीएपी से प्राप्त {dapCredit.toFixed(1)} kg नाइट्रोजन घटा दी गई है)*
              </td>
            </tr>
            <tr>
              <td className="border border-black p-2 font-bold">म्यूरिएट ऑफ पोटाश (MOP)</td>
              <td className="border border-black p-2 text-center font-black text-sm">{mopBags.toFixed(1)} बोरी (50kg)</td>
              <td className="border border-black p-2 text-center">{Math.round(mopBags * 50)} किग्रा</td>
              <td className="border border-black p-2">बुवाई के समय डीएपी के साथ मिलाकर दें।</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Safety & Advisory Summary */}
      <div className="py-3 border-t border-gray-400 text-xs space-y-1.5">
        <h4 className="font-bold">2. मौसम व सुरक्षा चेतावनी:</h4>
        <p className="text-gray-800">
          {advisory.farmer_summary || 'सटीक मौसम व मिट्टी जांच के आधार पर संतुलित उर्वरक का प्रयोग करें। तेज बारिश होने पर यूरिया का छिड़काव रोकें।'}
        </p>
      </div>

      {/* Verification footer */}
      <div className="pt-6 border-t border-black flex justify-between items-end text-[10px] text-gray-600">
        <div>
          <p>KhetSathi 360 · राष्ट्रीय कृषि निर्णय प्रणाली</p>
          <p>निःशुल्क किसान हेल्पलाइन: 1800-180-1551</p>
          <p>पोर्टल: https://khetsathi-360.onrender.com</p>
        </div>
        <div className="text-right border-t border-black pt-1 px-4">
          <p className="font-bold text-black">प्राधिकृत डिजिटल संस्तुति</p>
          <p>KhetSathi Agronomy Engine</p>
        </div>
      </div>
    </div>
  );
};
