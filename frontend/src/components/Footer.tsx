import React from 'react';
import { Activity, ShieldAlert } from 'lucide-react';
import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface FooterProps {
  language: LanguageChoice;
}

export const Footer: React.FC<FooterProps> = ({ language }) => {
  const t = translations[language].footer;

  return (
    <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-800 pb-8">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <span className="font-extrabold text-base text-white tracking-tight">
                HealthGuide AI
              </span>
              <p className="text-slate-400 text-xs">
                Understand symptoms. Recognize warning signs. Take safer next steps.
              </p>
            </div>
          </div>
          <div className="text-slate-400 font-medium text-center sm:text-right">
            UnivaBio 2026 Hackathon Prototype
          </div>
        </div>

        <div className="flex items-start gap-3 p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 text-slate-300">
          <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <p className="leading-relaxed">{t.disclaimer}</p>
        </div>

        <div className="text-center text-slate-500 text-xs">
          © 2026 HealthGuide AI. {t.rights}
        </div>
      </div>
    </footer>
  );
};
