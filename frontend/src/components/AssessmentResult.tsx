import React from 'react';
import {
  AlertOctagon,
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  Clock,
  ExternalLink,
  HeartPulse,
  Info,
  PhoneCall,
  Printer,
  ShieldCheck,
  Stethoscope,
} from 'lucide-react';
import { AssessmentResponse, LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface AssessmentResultProps {
  language: LanguageChoice;
  result: AssessmentResponse;
  onReset: () => void;
  onEdit: () => void;
}

export const AssessmentResult: React.FC<AssessmentResultProps> = ({
  language,
  result,
  onReset,
  onEdit,
}) => {
  const t = translations[language].results;

  const isEmergency = result.urgency_level === 'EMERGENCY' || result.is_emergency;

  // Status Styling Configuration
  const urgencyStyles = {
    EMERGENCY: {
      badgeBg: 'bg-rose-100 text-rose-900 border-rose-300',
      heroBg: 'bg-rose-600 text-white',
      cardBorder: 'border-rose-300 ring-4 ring-rose-50',
      icon: AlertOctagon,
    },
    SEEK_CARE_SOON: {
      badgeBg: 'bg-amber-100 text-amber-900 border-amber-300',
      heroBg: 'bg-amber-600 text-white',
      cardBorder: 'border-amber-300 ring-4 ring-amber-50',
      icon: AlertTriangle,
    },
    SELF_CARE_MONITOR: {
      badgeBg: 'bg-teal-100 text-teal-900 border-teal-300',
      heroBg: 'bg-teal-700 text-white',
      cardBorder: 'border-teal-300 ring-4 ring-teal-50',
      icon: CheckCircle2,
    },
    AMBIGUOUS_CONSULT_CLINICIAN: {
      badgeBg: 'bg-slate-100 text-slate-800 border-slate-300',
      heroBg: 'bg-slate-800 text-white',
      cardBorder: 'border-slate-300 ring-4 ring-slate-50',
      icon: Info,
    },
  }[result.urgency_level];

  const StatusIcon = urgencyStyles.icon;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div id="assessment-result" className="max-w-4xl mx-auto px-4 sm:px-6 my-10 animate-fadeIn">
      {/* 1. Prominent Urgency Header Banner */}
      <div
        className={`rounded-2xl p-6 sm:p-8 mb-8 shadow-md ${urgencyStyles.heroBg}`}
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start sm:items-center gap-3.5">
            <div className="p-3 bg-white/20 rounded-2xl shrink-0 backdrop-blur-xs">
              <StatusIcon className="w-8 h-8" />
            </div>
            <div>
              <span className="inline-block text-[11px] font-extrabold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-white/20 text-white mb-1.5">
                {t.disclaimerBadge}
              </span>
              <h2 className="text-xl sm:text-3xl font-extrabold tracking-tight">
                {t.urgencyLevels[result.urgency_level]}
              </h2>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-center">
            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-white/15 hover:bg-white/25 text-white transition backdrop-blur-xs"
              title="Print Summary"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>{t.printBtn}</span>
            </button>
          </div>
        </div>

        {/* Emergency Notice Box (If emergency flagged) */}
        {isEmergency && result.emergency_notice && (
          <div className="mt-6 pt-6 border-t border-white/20 space-y-4">
            <p className="text-sm sm:text-base leading-relaxed font-medium bg-black/10 p-4 rounded-xl border border-white/20">
              {result.emergency_notice.message}
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <span className="text-xs font-bold uppercase tracking-wider text-white/90">
                {language === 'ta' ? 'அவசர எண்கள்:' : 'Emergency Hotlines:'}
              </span>
              {result.emergency_notice.emergency_numbers.map((num, i) => (
                <a
                  key={i}
                  href={`tel:${num.split(' ')[0]}`}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white text-rose-800 font-extrabold rounded-lg text-xs hover:bg-rose-50 transition shadow-xs"
                >
                  <PhoneCall className="w-3.5 h-3.5" />
                  {num}
                </a>
              ))}
            </div>

            {result.emergency_notice.warning_signs_detected.length > 0 && (
              <div className="bg-white/10 p-3.5 rounded-xl text-xs space-y-1">
                <span className="font-bold uppercase tracking-wider text-rose-100 block">
                  {language === 'ta'
                    ? 'கண்டறியப்பட்ட அவசர அறிகுறிகள்:'
                    : 'Critical Warning Signs Detected:'}
                </span>
                <ul className="list-disc list-inside space-y-0.5 text-white/95">
                  {result.emergency_notice.warning_signs_detected.map((w, idx) => (
                    <li key={idx} className="font-semibold">{w}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="space-y-6">
        {/* 2. What the system noticed */}
        {result.observed_signals.length > 0 && (
          <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
            <div className="flex items-center gap-2.5 mb-2">
              <div className="p-2 rounded-xl bg-teal-50 text-teal-700">
                <HeartPulse className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
                  {t.signalsHeader}
                </h3>
                <p className="text-xs text-slate-500">{t.signalsSub}</p>
              </div>
            </div>

            <div className="mt-4 space-y-2.5">
              {result.observed_signals.map((sig, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 text-xs sm:text-sm"
                >
                  <div className="font-bold text-slate-900 mb-0.5">
                    {sig.label}
                  </div>
                  <div className="text-slate-600 leading-relaxed">
                    {sig.description}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 3. General Possible Explanations (Curated Educational Only) */}
        {result.possible_explanations.length > 0 && (
          <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
            <div className="flex items-center gap-2.5 mb-2">
              <div className="p-2 rounded-xl bg-blue-50 text-blue-700">
                <Stethoscope className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
                  {t.explanationsHeader}
                </h3>
                <p className="text-xs text-slate-500">{t.explanationsSub}</p>
              </div>
            </div>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.possible_explanations.map((exp, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between"
                >
                  <div>
                    <h4 className="font-bold text-slate-900 text-sm mb-1">
                      {exp.title}
                    </h4>
                    <p className="text-xs text-slate-600 leading-relaxed mb-3">
                      {exp.description}
                    </p>
                  </div>
                  <div className="text-[11px] text-slate-500 bg-white p-2.5 rounded-lg border border-slate-200 leading-normal">
                    <span className="font-semibold text-slate-700">Context: </span>
                    {exp.educational_context}
                  </div>
                </div>
              ))}
            </div>

            {/* Uncertainty statement */}
            <div className="mt-4 p-3.5 rounded-xl bg-amber-50/60 border border-amber-200/80 text-amber-900 text-xs flex items-start gap-2.5 leading-relaxed">
              <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <span>{result.uncertainty_notice}</span>
            </div>
          </div>
        )}

        {/* 4. Safe Low-Risk Self-Care Guidance (Only when appropriate and low-risk) */}
        {result.self_care_guidance.length > 0 && !isEmergency && (
          <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
            <div className="flex items-center gap-2.5 mb-2">
              <div className="p-2 rounded-xl bg-emerald-50 text-emerald-700">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
                  {t.selfCareHeader}
                </h3>
                <p className="text-xs text-slate-500">{t.selfCareSub}</p>
              </div>
            </div>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
              {result.self_care_guidance.map((care, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl border border-emerald-100 bg-emerald-50/30 text-xs"
                >
                  <div className="font-bold text-emerald-900 uppercase tracking-wider text-[11px] mb-1">
                    {care.category}
                  </div>
                  <div className="text-slate-700 leading-relaxed">{care.tip}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 5. Recommended Next Steps */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
          <div className="flex items-center gap-2.5 mb-4">
            <div className="p-2 rounded-xl bg-indigo-50 text-indigo-700">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
                {t.nextStepsHeader}
              </h3>
            </div>
          </div>

          <ul className="space-y-2.5 text-sm">
            {result.next_steps.map((step, idx) => (
              <li
                key={idx}
                className="flex items-start gap-3 p-3 rounded-xl bg-slate-50 border border-slate-100 text-slate-800"
              >
                <div className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                  {idx + 1}
                </div>
                <span className="leading-relaxed">{step}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 6. Trusted Medical References (MedlinePlus & NHS) */}
        {result.trusted_sources.length > 0 && (
          <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
            <div className="mb-4">
              <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
                {t.trustedSourcesHeader}
              </h3>
              <p className="text-xs text-slate-500">{t.sourcesNote}</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {result.trusted_sources.map((src, idx) => (
                <a
                  key={idx}
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-4 rounded-xl border border-slate-200 hover:border-teal-400 bg-slate-50/50 hover:bg-teal-50/30 transition group flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className="font-bold text-slate-900 text-sm group-hover:text-teal-900">
                        {src.name}
                      </span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-teal-600 shrink-0" />
                    </div>
                    <p className="text-xs text-slate-600 leading-normal mb-2">
                      {src.description}
                    </p>
                  </div>
                  <span className="text-[11px] font-medium text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200/60 self-start">
                    {src.relevance_note}
                  </span>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* 7. Action Controls: Edit symptoms & Check Another */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4">
          <button
            type="button"
            onClick={onEdit}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-sm shadow-2xs transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>{translations[language].form.editBtn}</span>
          </button>
          <button
            type="button"
            onClick={onReset}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-bold text-sm shadow-sm transition"
          >
            <HeartPulse className="w-4 h-4" />
            <span>{t.tryAnotherBtn}</span>
          </button>
        </div>

        {/* 8. Non-Diagnostic Medical Disclaimer Footer Card */}
        <div className="mt-8 p-4 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 text-xs text-center leading-relaxed">
          {result.disclaimer}
        </div>
      </div>
    </div>
  );
};
