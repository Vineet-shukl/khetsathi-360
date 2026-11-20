import React from 'react';

export type TabId = 'advisory' | 'soil_card' | 'organic' | 'community';

interface NavigationTabsProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
  isHi: boolean;
}

export const NavigationTabs: React.FC<NavigationTabsProps> = ({
  activeTab,
  onTabChange,
  isHi,
}) => {
  const tabs: { id: TabId; icon: string; title_hi: string; title_en: string; badge?: string }[] = [
    {
      id: 'advisory',
      icon: '🌾',
      title_hi: 'किसान सलाह पर्ची',
      title_en: 'Advisory Slip',
    },
    {
      id: 'soil_card',
      icon: '🧪',
      title_hi: 'मृदा कार्ड व लैब OCR',
      title_en: 'Soil Health & OCR',
      badge: isHi ? 'विजन AI' : 'Vision AI',
    },
    {
      id: 'organic',
      icon: '🌿',
      title_hi: 'जैविक खेती व बाजार',
      title_en: 'Organic & Subsidy',
      badge: 'PKVY',
    },
    {
      id: 'community',
      icon: '🤝',
      title_hi: 'स्थानीय किसान समुदाय',
      title_en: 'Connect Farmers',
      badge: isHi ? 'लाइव' : 'Live',
    },
  ];

  return (
    <nav
      role="tablist"
      aria-label={isHi ? 'मुख्य मॉड्यूल नेविगेशन' : 'Main Module Navigation'}
      className="flex items-center gap-2 p-1.5 bg-[#f4efe6] rounded-2xl border border-[#e6dfd3] overflow-x-auto scrollbar-none shadow-xs"
    >
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            role="tab"
            aria-selected={isActive}
            aria-controls={`tabpanel-${tab.id}`}
            tabIndex={isActive ? 0 : -1}
            onClick={() => onTabChange(tab.id)}
            className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 whitespace-nowrap transition-all duration-150 cursor-pointer select-none ${
              isActive
                ? 'bg-[#143826] text-white shadow-sm ring-1 ring-[#143826]'
                : 'text-[#3d4b43] hover:text-[#143826] hover:bg-white/60'
            }`}
          >
            <span className="text-base" aria-hidden="true">
              {tab.icon}
            </span>
            <span>{isHi ? tab.title_hi : tab.title_en}</span>
            {tab.badge && (
              <span
                className={`text-[9px] font-extrabold uppercase px-1.5 py-0.5 rounded-full ${
                  isActive
                    ? 'bg-[#c96442] text-white'
                    : 'bg-emerald-100 text-emerald-900 border border-emerald-300'
                }`}
              >
                {tab.badge}
              </span>
            )}
          </button>
        );
      })}
    </nav>
  );
};
