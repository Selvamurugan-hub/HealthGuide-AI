import React from 'react';
import { ShieldCheck, AlertOctagon, BookOpen, Lock } from 'lucide-react';
import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface HowItWorksProps {
  language: LanguageChoice;
}

export const HowItWorks: React.FC<HowItWorksProps> = ({ language }) => {
  const t = translations[language].howItWorks;

  const steps = [
    {
      icon: AlertOctagon,
      title: t.step1Title,
      desc: t.step1Desc,
      color: 'bg-rose-50 text-rose-700 border-rose-200',
    },
    {
      icon: ShieldCheck,
      title: t.step2Title,
      desc: t.step2Desc,
      color: 'bg-teal-50 text-teal-700 border-teal-200',
    },
    {
      icon: BookOpen,
      title: t.step3Title,
      desc: t.step3Desc,
      color: 'bg-blue-50 text-blue-700 border-blue-200',
    },
    {
      icon: Lock,
      title: t.step4Title,
      desc: t.step4Desc,
      color: 'bg-slate-50 text-slate-700 border-slate-200',
    },
  ];

  return (
    <section id="how-it-works" className="py-16 bg-white border-t border-slate-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mb-3">
            {t.title}
          </h2>
          <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
            {t.subtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((st, i) => {
            const Icon = st.icon;
            return (
              <div
                key={i}
                className="bg-slate-50/70 border border-slate-200/80 rounded-2xl p-6 flex flex-col justify-between shadow-2xs hover:shadow-xs transition"
              >
                <div>
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center mb-5 border ${st.color}`}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="font-bold text-slate-900 text-base mb-2">
                    {st.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    {st.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
