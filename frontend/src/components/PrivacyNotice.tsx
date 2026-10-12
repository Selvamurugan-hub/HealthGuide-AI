import React from 'react';
import { Lock, Shield, EyeOff, Server } from 'lucide-react';
import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface PrivacyNoticeProps {
  language: LanguageChoice;
}

export const PrivacyNotice: React.FC<PrivacyNoticeProps> = ({ language }) => {
  const t = translations[language].privacySection;

  return (
    <section id="privacy" className="py-16 bg-white border-t border-slate-200">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-800 text-xs font-semibold mb-3">
            <Lock className="w-3.5 h-3.5 text-slate-600" />
            <span>{language === 'ta' ? 'தனியுரிமை கொள்கை' : 'Zero Persistence'}</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mb-3">
            {t.title}
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-sm">
            <div className="p-2.5 rounded-xl bg-teal-100 text-teal-800 w-fit mb-3">
              <EyeOff className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 mb-1">
              {language === 'ta' ? 'அடையாளக் கோரல் இல்லை' : 'No Identifiers'}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">{t.p1}</p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-sm">
            <div className="p-2.5 rounded-xl bg-blue-100 text-blue-800 w-fit mb-3">
              <Server className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 mb-1">
              {language === 'ta' ? 'தரவுத்தள சேமிப்பு இல்லை' : 'In-Memory Only'}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">{t.p2}</p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-sm">
            <div className="p-2.5 rounded-xl bg-emerald-100 text-emerald-800 w-fit mb-3">
              <Shield className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 mb-1">
              {language === 'ta' ? 'மறைக்கப்பட்ட பதிவுகள்' : 'Masked Logs'}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">{t.p3}</p>
          </div>
        </div>
      </div>
    </section>
  );
};
