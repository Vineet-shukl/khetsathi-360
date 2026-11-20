import React from 'react';
import type { WeatherForecastResponse } from '../types/contracts';

interface WeatherAlertBannerProps {
  weather?: WeatherForecastResponse;
  isHi: boolean;
}

export const WeatherAlertBanner: React.FC<WeatherAlertBannerProps> = ({ weather, isHi }) => {
  if (!weather) return null;

  return (
    <div className="space-y-3">
      {/* Heavy Rain / Weather Irregularity Alert */}
      {weather.hold_urea_action && (
        <div className="p-4 rounded-2xl bg-amber-500 text-amber-950 border-2 border-amber-600 shadow-sm flex items-start gap-3">
          <span className="relative flex h-3.5 w-3.5 mt-1 shrink-0">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-950 opacity-75" />
            <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-amber-950" />
          </span>
          <div className="space-y-1">
            <h4 className="text-sm font-black uppercase tracking-wide">
              {isHi ? '⚠️ भारी बारिश चेतावनी — यूरिया छिड़काव स्थगित रखें!' : '⚠️ Heavy Rain Alert — Hold Urea Top-Dressing!'}
            </h4>
            <p className="text-xs font-semibold leading-relaxed">
              {isHi
                ? `अगले 48 घंटों में भारी वर्षा की संभावना (${weather.rain_prob_48h_pct}% संभावना, ${weather.precipitation_sum_mm.toFixed(1)} मिमी अनुमान) है। यूरिया बहने (leaching) से बचाने हेतु छिड़काव रोकें।`
                : `Heavy rainfall expected in next 48h (${weather.rain_prob_48h_pct}% chance, ${weather.precipitation_sum_mm.toFixed(1)} mm). Postpone Urea to prevent nitrogen leaching.`}
            </p>
          </div>
        </div>
      )}

      {/* Weather Metrics Card */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
        <div className="p-3 rounded-xl bg-white border border-slate-200">
          <span className="text-slate-500 block text-[11px] font-medium">{isHi ? 'तापमान (Temp)' : 'Temperature'}</span>
          <span className="text-lg font-black text-slate-800">{weather.temp_c.toFixed(1)}°C</span>
        </div>
        <div className="p-3 rounded-xl bg-white border border-slate-200">
          <span className="text-slate-500 block text-[11px] font-medium">{isHi ? 'नमी (Humidity)' : 'Rel. Humidity'}</span>
          <span className="text-lg font-black text-slate-800">{weather.relative_humidity_pct}%</span>
        </div>
        <div className="p-3 rounded-xl bg-white border border-slate-200">
          <span className="text-slate-500 block text-[11px] font-medium">{isHi ? 'वर्षा सम्भावना (48h)' : 'Rain Prob (48h)'}</span>
          <span className="text-lg font-black text-slate-800">{weather.rain_prob_48h_pct}%</span>
        </div>
        <div className="p-3 rounded-xl bg-white border border-slate-200">
          <span className="text-slate-500 block text-[11px] font-medium">{isHi ? 'वाष्पोत्सर्जन (ET0)' : 'FAO-56 ET0'}</span>
          <span className="text-lg font-black text-blue-700">{weather.et0_fao_mm_day.toFixed(1)} mm/day</span>
        </div>
      </div>
    </div>
  );
};
