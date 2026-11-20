import React from 'react';
import type { IrrigationSchedule } from '../types/contracts';

interface IrrigationTimelineProps {
  schedule?: IrrigationSchedule;
  isHi: boolean;
}

export const IrrigationTimeline: React.FC<IrrigationTimelineProps> = ({ schedule, isHi }) => {
  if (!schedule || !schedule.stages || schedule.stages.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-blue-50/70 border border-blue-200 text-xs text-blue-900">
        {isHi
          ? '💧 सिंचाई समय सारणी: स्थानीय मिट्टी नमी के अनुसार सामान्य सिंचाई चक्र अनुशंसित है।'
          : '💧 Irrigation: Regular irrigation cycle recommended per local moisture levels.'}
      </div>
    );
  }

  return (
    <div className="p-5 rounded-2xl bg-white border border-blue-200 shadow-xs space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl">💧</span>
          <div>
            <h4 className="text-sm font-bold text-blue-950">
              {isHi ? 'सिंचाई कब करें (FAO-56 जल मांग चक्र)' : 'Irrigation Schedule (FAO-56 Water Demand)'}
            </h4>
            <p className="text-[11px] text-slate-500">
              {isHi ? 'फसल की क्रांतिक अवस्थाएं व जल अनुप्रयोग' : 'Critical growth stages and water depths'}
            </p>
          </div>
        </div>
        <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-blue-100 text-blue-900 border border-blue-300">
          {schedule.stages.length} {isHi ? 'सिंचाई चरण' : 'Stages'}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {schedule.stages.map((stage, idx) => (
          <div
            key={idx}
            className="p-3 rounded-xl bg-gradient-to-br from-blue-50/60 to-white border border-blue-200 space-y-1.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-blue-200 text-blue-900">
                {isHi ? `चरण ${idx + 1}` : `Stage ${idx + 1}`}
              </span>
              <span className="text-xs font-black text-blue-900">
                {stage.days_after_sowing} {isHi ? 'दिन' : 'Days'}
              </span>
            </div>
            <h5 className="text-xs font-bold text-slate-900">{stage.stage_name}</h5>
            <p className="text-[11px] text-slate-600 line-clamp-2">{stage.description}</p>
            <div className="text-[11px] font-bold text-blue-700 pt-1 border-t border-blue-100 flex items-center justify-between">
              <span>{isHi ? 'जल स्तर:' : 'Depth:'}</span>
              <span>{stage.depth_mm} mm</span>
            </div>
          </div>
        ))}
      </div>

      {schedule.notes && (
        <p className="text-[11px] text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
          📌 {schedule.notes}
        </p>
      )}
    </div>
  );
};
