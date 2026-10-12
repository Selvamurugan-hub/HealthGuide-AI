import React from 'react';
import { AlertCircle, ShieldAlert } from 'lucide-react';
import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface SafetyNoticeProps {
  language: LanguageChoice;
}

export const SafetyNotice: React.FC<SafetyNoticeProps> = ({ language }) => {
  const t = translations[language].safetyNotice;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 my-8">
      <div className="bg-amber-50/70 border border-amber-200 rounded-2xl p-5 shadow-2xs">
        <div className="flex items-start gap-4">
          <div className="p-2 rounded-xl bg-amber-100 text-amber-800 shrink-0 mt-0.5">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div className="text-sm space-y-1.5 text-amber-900">
            <h4 className="font-bold text-amber-950 text-sm tracking-tight flex items-center gap-1.5">
              <AlertCircle className="w-4 h-4 text-amber-700" />
              {t.title}
            </h4>
            <p className="leading-relaxed">{t.p1}</p>
            <p className="font-semibold text-amber-950">{t.p2}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
