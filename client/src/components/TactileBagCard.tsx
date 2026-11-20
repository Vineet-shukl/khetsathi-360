import React from 'react';

interface TactileBagCardProps {
  title: string;
  subtitle: string;
  bags: number;
  bagSizeKg: number;
  colorTheme: 'emerald' | 'amber' | 'blue';
  icon: string;
  timingNote: string;
  creditNote?: string;
}

export const TactileBagCard: React.FC<TactileBagCardProps> = ({
  title,
  subtitle,
  bags,
  bagSizeKg,
  colorTheme,
  icon,
  timingNote,
  creditNote,
}) => {
  const themeStyles = {
    emerald: {
      border: 'border-emerald-600',
      badge: 'bg-emerald-100 text-emerald-900 border-emerald-300',
      counter: 'text-emerald-950',
      bar: 'bg-emerald-600',
    },
    amber: {
      border: 'border-amber-600',
      badge: 'bg-amber-100 text-amber-950 border-amber-300',
      counter: 'text-amber-950',
      bar: 'bg-amber-600',
    },
    blue: {
      border: 'border-blue-600',
      badge: 'bg-blue-100 text-blue-950 border-blue-300',
      counter: 'text-blue-950',
      bar: 'bg-blue-600',
    },
  }[colorTheme];

  return (
    <div
      className={`relative p-5 rounded-2xl bg-white border-2 ${themeStyles.border} shadow-sm transition hover:shadow-md space-y-3`}
    >
      <div className="flex items-center justify-between">
        <span className="text-2xl" aria-hidden="true">
          {icon}
        </span>
        <span className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-full border ${themeStyles.badge}`}>
          {bagSizeKg} kg बोरी
        </span>
      </div>

      <div>
        <h4 className="text-sm font-bold text-slate-800">{title}</h4>
        <p className="text-[11px] text-slate-500 font-medium">{subtitle}</p>
      </div>

      <div className="pt-2 border-t border-slate-100 flex items-baseline justify-between">
        <div>
          <span className={`text-4xl font-black ${themeStyles.counter}`}>
            {bags.toFixed(1)}
          </span>
          <span className="text-xs font-bold text-slate-600 ml-1.5">बोरी (Bags)</span>
        </div>
        <span className="text-[11px] text-slate-500 font-semibold">
          ≈ {Math.round(bags * bagSizeKg)} कि.ग्रा.
        </span>
      </div>

      <p className="text-[11px] text-slate-600 leading-relaxed font-medium bg-slate-50 p-2 rounded-lg border border-slate-200/60">
        📌 {timingNote}
      </p>

      {creditNote && (
        <p className="text-[10px] text-emerald-800 font-bold bg-emerald-50/80 p-1.5 rounded border border-emerald-200">
          💡 {creditNote}
        </p>
      )}
    </div>
  );
};
