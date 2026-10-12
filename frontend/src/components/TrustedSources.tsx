import React from 'react';
import { ExternalLink, CheckCircle, ShieldCheck } from 'lucide-react';
import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface TrustedSourcesProps {
  language: LanguageChoice;
}

export const TrustedSources: React.FC<TrustedSourcesProps> = ({ language }) => {
  const t = translations[language].sourcesSection;

  return (
    <section id="sources" className="py-16 bg-slate-50 border-t border-slate-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold mb-3">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
            <span>{language === 'ta' ? 'அங்கீகரிக்கப்பட்ட தளங்கள்' : 'Clinical References'}</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mb-3">
            {t.title}
          </h2>
          <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
            {t.subtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* MedlinePlus Card */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 flex flex-col justify-between shadow-2xs hover:shadow-sm transition">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-md bg-blue-50 text-blue-800 border border-blue-200">
                  National Institutes of Health (US)
                </span>
                <CheckCircle className="w-5 h-5 text-teal-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">
                {t.medlinePlusTitle}
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed mb-6">
                {t.medlinePlusDesc}
              </p>
            </div>
            <a
              href="https://medlineplus.gov/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm font-bold text-teal-700 hover:text-teal-800 transition self-start"
            >
              <span>{t.visitSource} (medlineplus.gov)</span>
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>

          {/* NHS Health A to Z Card */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 flex flex-col justify-between shadow-2xs hover:shadow-sm transition">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-800 border border-indigo-200">
                  National Health Service (UK)
                </span>
                <CheckCircle className="w-5 h-5 text-teal-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">
                {t.nhsTitle}
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed mb-6">
                {t.nhsDesc}
              </p>
            </div>
            <a
              href="https://www.nhs.uk/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm font-bold text-teal-700 hover:text-teal-800 transition self-start"
            >
              <span>{t.visitSource} (nhs.uk)</span>
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};
