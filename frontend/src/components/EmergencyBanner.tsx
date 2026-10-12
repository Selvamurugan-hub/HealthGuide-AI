import React from 'react';
import { AlertTriangle, PhoneCall } from 'lucide-react';
import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface EmergencyBannerProps {
  language: LanguageChoice;
}

export const EmergencyBanner: React.FC<EmergencyBannerProps> = ({ language }) => {
  const t = translations[language].hero;

  return (
    <div className="bg-rose-600 text-white px-4 py-3 shadow-sm">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-sm">
        <div className="flex items-center gap-2.5 font-medium text-center sm:text-left">
          <AlertTriangle className="w-5 h-5 text-rose-200 shrink-0 animate-pulse" />
          <span>{t.emergencyStrip}</span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <a
            href="tel:112"
            className="inline-flex items-center gap-1.5 px-3 py-1 bg-white text-rose-700 font-bold rounded-lg text-xs hover:bg-rose-50 transition shadow-xs"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            112 / 911 / 108
          </a>
        </div>
      </div>
    </div>
  );
};
