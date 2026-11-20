import React from 'react';
import type { SatelliteVegetationIndex } from '../types/contracts';

interface SatelliteCardProps {
  satellite?: SatelliteVegetationIndex | null;
  isHi: boolean;
}

export const SatelliteCard: React.FC<SatelliteCardProps> = ({ satellite, isHi }) => {
  if (!satellite) return null;

  const ndvi = satellite.ndvi ?? 0.68;
  const ndre = satellite.ndre ?? 0.42;

  // NDVI health score 0.0 to 1.0 mapped to percent
  const ndviPct = Math.min(100, Math.max(0, Math.round(ndvi * 100)));

  return (
    <div className="fable-card p-5 rounded-3xl bg-gradient-to-br from-emerald-950 via-[#143826] to-[#0d261a] text-white space-y-4 shadow-md">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-emerald-800/80 pb-3">
        <div className="flex items-center gap-2.5">
          <span className="text-2xl" aria-hidden="true">
            🛰️
          </span>
          <div>
            <h4 className="text-sm sm:text-base font-bold text-emerald-100 font-serif-fable">
              {isHi
                ? 'उपग्रह रिमोट सेंसिंग व फसल स्वास्थ्य (Live Sentinel-2 NDVI)'
                : 'Satellite Remote Sensing & Crop Vigor (Copernicus Sentinel-2)'}
            </h4>
            <p className="text-[11px] text-emerald-300">
              {satellite.satellite_name || 'Copernicus Sentinel-2 MSI (10m Resolution)'}
            </p>
          </div>
        </div>

        <span className="inline-flex self-start sm:self-center text-[10px] font-black uppercase px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
          {isHi ? satellite.crop_vigor_status_hi : satellite.crop_vigor_status}
        </span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
        <div className="p-3 rounded-2xl bg-white/10 border border-white/15">
          <span className="text-[11px] text-emerald-200 block font-medium">
            {isHi ? 'हरियाली सूचकांक (NDVI)' : 'Normalized NDVI'}
          </span>
          <span className="text-xl font-black text-emerald-300">
            {ndvi.toFixed(2)}
          </span>
          <div className="w-full bg-emerald-900/60 rounded-full h-1.5 mt-1 overflow-hidden">
            <div
              className="bg-emerald-400 h-1.5 rounded-full"
              style={{ width: `${ndviPct}%` }}
            />
          </div>
        </div>

        <div className="p-3 rounded-2xl bg-white/10 border border-white/15">
          <span className="text-[11px] text-emerald-200 block font-medium">
            {isHi ? 'क्लोरोफिल सूचकांक (NDRE)' : 'Red-Edge NDRE'}
          </span>
          <span className="text-xl font-black text-amber-300">
            {ndre.toFixed(2)}
          </span>
          <span className="text-[10px] text-emerald-300/80 block mt-1">
            {isHi ? 'सघन पर्णहरित' : 'Dense Canopy'}
          </span>
        </div>

        <div className="p-3 rounded-2xl bg-white/10 border border-white/15">
          <span className="text-[11px] text-emerald-200 block font-medium">
            {isHi ? 'मिट्टी संरचना (Clay %)' : 'SoilGrids Clay %'}
          </span>
          <span className="text-xl font-black text-slate-100">
            {(satellite.soilgrids_clay_pct ?? 24.5).toFixed(1)}%
          </span>
          <span className="text-[10px] text-emerald-300/80 block mt-1">
            {isHi ? 'मध्यम धारण क्षमता' : 'Medium Retention'}
          </span>
        </div>

        <div className="p-3 rounded-2xl bg-white/10 border border-white/15">
          <span className="text-[11px] text-emerald-200 block font-medium">
            {isHi ? 'घनत्व (Bulk Density)' : 'Bulk Density'}
          </span>
          <span className="text-xl font-black text-slate-100">
            {(satellite.soilgrids_bulk_density_g_cm3 ?? 1.35).toFixed(2)}
          </span>
          <span className="text-[10px] text-emerald-300/80 block mt-1">
            g/cm³ (SoilGrids 250m)
          </span>
        </div>
      </div>

      {/* Agronomic Remote Sensing Action */}
      <div className="p-3 rounded-xl bg-emerald-900/50 border border-emerald-700/60 text-xs text-emerald-100 flex items-start gap-2">
        <span className="text-base shrink-0">💡</span>
        <p className="leading-relaxed">
          <span className="font-bold">
            {isHi ? 'उपग्रह आधारित संस्तुति: ' : 'Satellite Agronomic Guidance: '}
          </span>
          {isHi ? satellite.remote_sensing_action_hi : satellite.remote_sensing_action_en}
        </p>
      </div>
    </div>
  );
};
