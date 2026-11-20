import React, { useState } from 'react';
import type { AdvisoryResponse } from '../types/contracts';

interface ScientificConsoleProps {
  advisory: AdvisoryResponse;
  isHi: boolean;
}

export const ScientificConsole: React.FC<ScientificConsoleProps> = ({ advisory, isHi }) => {
  const [isOpen, setIsOpen] = useState(false);

  const targets = advisory.elemental_target_kg || {};
  const deltaN = advisory.ml_residual_delta_n_kg_ha ?? 0;
  const confBand = advisory.ml_confidence_band_kg_ha || [0, 0];

  return (
    <div className="fable-card rounded-2xl border border-[#e6dfd3] overflow-hidden">
      {/* Toggle button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        className="w-full p-4 bg-[#f4efe6] hover:bg-[#eae3d5] text-[#143826] font-bold text-xs sm:text-sm flex items-center justify-between transition cursor-pointer select-none"
      >
        <div className="flex items-center gap-2">
          <span className="text-lg">🔬</span>
          <span className="font-serif-fable text-sm sm:text-base">
            {isHi ? 'वैज्ञानिक मोड — ICAR सूत्र व ML सांख्यिकी' : 'Scientific Mode — ICAR Math & ML Telemetry'}
          </span>
          <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded-full bg-[#143826] text-white">
            {advisory.serving_mode || 'Hybrid ML'}
          </span>
        </div>

        <span className="text-sm font-extrabold text-[#143826]">
          {isOpen ? '▲ ' + (isHi ? 'छिपाएं' : 'Hide') : '▼ ' + (isHi ? 'विस्तार देखें' : 'Expand')}
        </span>
      </button>

      {/* Expanded Scientific Content */}
      {isOpen && (
        <div className="p-5 space-y-4 bg-white border-t border-[#e6dfd3] text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="p-3 rounded-xl bg-[#faf8f5] border border-[#e6dfd3]">
              <span className="text-[11px] text-[#5f6b64] font-bold block">
                {isHi ? 'तत्वीय लक्ष्य (Elemental Targets)' : 'Elemental Targets (kg/ha)'}
              </span>
              <div className="mt-1 font-mono font-bold text-[#143826] space-y-0.5">
                <div>N: {targets.n_kg ?? 120} kg</div>
                <div>P₂O₅: {targets.p_kg ?? 60} kg</div>
                <div>K₂O: {targets.k_kg ?? 40} kg</div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-[#faf8f5] border border-[#e6dfd3]">
              <span className="text-[11px] text-[#5f6b64] font-bold block">
                {isHi ? 'ML अवशिष्ट संशोधन (ML Residual Delta)' : 'ML Residual Delta N'}
              </span>
              <div className="mt-1 font-mono font-bold text-[#143826]">
                ΔN: {deltaN > 0 ? `+${deltaN.toFixed(2)}` : deltaN.toFixed(2)} kg/ha
              </div>
              <p className="text-[10px] text-slate-500 mt-0.5">
                90% CI: [{confBand[0]?.toFixed(1)}, {confBand[1]?.toFixed(1)}] kg/ha
              </p>
            </div>

            <div className="p-3 rounded-xl bg-[#faf8f5] border border-[#e6dfd3]">
              <span className="text-[11px] text-[#5f6b64] font-bold block">
                {isHi ? 'मॉडल अनिश्चितता (Model Uncertainty)' : 'Model Uncertainty Margin'}
              </span>
              <div className="mt-1 font-mono font-bold text-amber-800 text-sm">
                ±{(advisory.uncertainty_pct ?? 12).toFixed(1)}%
              </div>
              <span className="text-[10px] text-[#5f6b64] block">
                {advisory.confidence_mode === 'shc_verified' ? 'मृदा कार्ड सत्यापित (SHC Verified)' : 'क्षेत्रीय आधार रेखा (Baseline)'}
              </span>
            </div>
          </div>

          {/* Sources and Data Provenance */}
          <div className="p-3 bg-[#faf8f5] rounded-xl border border-[#e6dfd3] space-y-1">
            <span className="text-[11px] font-bold text-[#143826] block">
              📚 {isHi ? 'वैज्ञानिक संदर्भ व डेटा स्रोत:' : 'Agronomic References & Provenance:'}
            </span>
            <ul className="list-disc list-inside text-[11px] text-[#5f6b64] space-y-0.5">
              {(advisory.sources || [
                'ICAR Package of Practices for Field Crops (Zone 4/UP Plain)',
                'FAO Irrigation and Drainage Paper No. 56 (Crop Evapotranspiration)',
                'DAC&FW Soil Health Management Norms & SoilGrids 250m Global Matrix',
              ]).map((src, i) => (
                <li key={i}>{src}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
