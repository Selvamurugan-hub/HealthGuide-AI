import React from 'react';
import { AlertOctagon, CheckCircle2, HelpCircle, Sparkles } from 'lucide-react';
import { AgeRange, DurationCategory, LanguageChoice, SeverityLevel, SymptomAssessmentRequest } from '../types';
import { translations } from '../i18n/translations';

interface DemoPresetsProps {
  language: LanguageChoice;
  onSelectPreset: (preset: SymptomAssessmentRequest) => void;
}

export const DemoPresets: React.FC<DemoPresetsProps> = ({
  language,
  onSelectPreset,
}) => {
  const t = translations[language].demo;

  const presets = [
    {
      id: 'emergency',
      title: t.emergencyTitle,
      desc: t.emergencyDesc,
      icon: AlertOctagon,
      badgeColor: 'bg-rose-100 text-rose-800 border-rose-300',
      btnColor: 'hover:border-rose-400 hover:bg-rose-50/40',
      data: {
        age_range: 'ADULT_18_64' as AgeRange,
        symptoms_text:
          language === 'ta'
            ? 'திடீரென கடுமையான நெஞ்சு வலி மற்றும் இடது கையில் பாரமான அழுத்தம் ஏற்படுகிறது, மூச்சு விட மிகவும் சிரமமாக உள்ளது.'
            : 'Severe crushing chest pain radiating to my left arm and jaw for the last 45 minutes with heavy chest pressure and shortness of breath.',
        duration: 'LESS_THAN_24_HOURS' as DurationCategory,
        severity: 'CRITICAL' as SeverityLevel,
        additional_context:
          language === 'ta'
            ? 'முன்பு மாரடைப்பு ஏற்பட்டதில்லை; ரத்த அழுத்தக் குறைவு இருக்கலாம்.'
            : 'Fictional demo case: No previous cardiac history; sudden acute onset.',
        language,
      },
    },
    {
      id: 'routine',
      title: t.routineTitle,
      desc: t.routineDesc,
      icon: CheckCircle2,
      badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      btnColor: 'hover:border-teal-400 hover:bg-teal-50/40',
      data: {
        age_range: 'ADULT_18_64' as AgeRange,
        symptoms_text:
          language === 'ta'
            ? 'இரண்டு நாட்களாக லேசான தலைவலி உள்ளது, கணினித் திரையை நீண்ட நேரம் பார்த்ததால் கழுத்துத் தசை இறுக்கமாக உணர்கிறேன்.'
            : 'Mild tension headache across my forehead and tight neck muscles for 2 days after working extended hours on a monitor.',
        duration: 'DAYS_1_TO_3' as DurationCategory,
        severity: 'MILD' as SeverityLevel,
        additional_context:
          language === 'ta'
            ? 'காய்ச்சல் அல்லது பார்வை மங்குதல் போன்ற வேறு அறிகுறிகள் இல்லை.'
            : 'Fictional demo case: No fever, vision normal, hydrated adequately.',
        language,
      },
    },
    {
      id: 'ambiguous',
      title: t.ambiguousTitle,
      desc: t.ambiguousDesc,
      icon: HelpCircle,
      badgeColor: 'bg-blue-100 text-blue-800 border-blue-300',
      btnColor: 'hover:border-blue-400 hover:bg-blue-50/40',
      data: {
        age_range: 'ADULT_18_64' as AgeRange,
        symptoms_text:
          language === 'ta'
            ? 'இடது காலில் கடந்த ஒரு வாரமாக விட்டு விட்டு லேசான மரத்துப்போன உணர்வு ஏற்படுகிறது, வலி இல்லை.'
            : 'Intermittent mild tingling sensation in my left foot when sitting for a few days, without pain or skin swelling.',
        duration: 'DAYS_4_TO_7' as DurationCategory,
        severity: 'MILD' as SeverityLevel,
        additional_context:
          language === 'ta'
            ? 'காயம் எதுவும் ஏற்படவில்லை.'
            : 'Fictional demo case: No recent injury or trauma recorded.',
        language,
      },
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 mb-8">
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-teal-600" />
            <h3 className="font-bold text-slate-900 text-base">{t.title}</h3>
          </div>
          <span className="text-[11px] font-bold tracking-wider px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200 uppercase self-start sm:self-auto">
            {t.fictionalBadge}
          </span>
        </div>

        <p className="text-xs sm:text-sm text-slate-600 mb-4">{t.subtitle}</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {presets.map((p) => {
            const Icon = p.icon;
            return (
              <button
                key={p.id}
                type="button"
                onClick={() => onSelectPreset(p.data)}
                className={`flex flex-col text-left p-4 rounded-xl border border-slate-200 bg-white ${p.btnColor} transition duration-150 group shadow-2xs hover:shadow-sm`}
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="p-1.5 rounded-lg bg-slate-50 group-hover:bg-white text-slate-700">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span
                    className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${p.badgeColor}`}
                  >
                    Preset
                  </span>
                </div>
                <h4 className="font-bold text-slate-900 text-xs sm:text-sm mb-1 group-hover:text-teal-900">
                  {p.title}
                </h4>
                <p className="text-xs text-slate-500 leading-normal mb-3 grow">
                  {p.desc}
                </p>
                <span className="text-xs font-semibold text-teal-700 group-hover:underline">
                  {t.loadBtn} →
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
