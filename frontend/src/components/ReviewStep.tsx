import React from 'react';
import { ArrowLeft, CheckCircle2, Edit3, ShieldAlert } from 'lucide-react';
import { LanguageChoice, SymptomAssessmentRequest } from '../types';
import { translations } from '../i18n/translations';

interface ReviewStepProps {
  language: LanguageChoice;
  data: SymptomAssessmentRequest;
  isLoading: boolean;
  onEdit: () => void;
  onConfirm: () => void;
}

export const ReviewStep: React.FC<ReviewStepProps> = ({
  language,
  data,
  isLoading,
  onEdit,
  onConfirm,
}) => {
  const t = translations[language].review;
  const formT = translations[language].form;

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 my-8 animate-fadeIn">
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 sm:p-8 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
          <div>
            <div className="text-teal-700 text-xs font-bold uppercase tracking-wider mb-1">
              {formT.step2Title}
            </div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
              {t.title}
            </h2>
          </div>
          <button
            type="button"
            onClick={onEdit}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition"
          >
            <Edit3 className="w-3.5 h-3.5" />
            <span>{t.backToEdit}</span>
          </button>
        </div>

        <p className="text-sm text-slate-600 mb-6">{t.subtitle}</p>

        {/* Summary Card */}
        <div className="space-y-4 bg-slate-50/70 border border-slate-200/80 rounded-xl p-5 mb-8">
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
              {t.age}
            </span>
            <div className="text-sm font-semibold text-slate-900">
              {formT.ages[data.age_range]}
            </div>
          </div>

          <div className="border-t border-slate-200/60 pt-3">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
              {t.symptoms}
            </span>
            <div className="text-sm text-slate-800 bg-white p-3 rounded-lg border border-slate-200 leading-relaxed font-mono">
              "{data.symptoms_text}"
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-slate-200/60 pt-3">
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
                {t.duration}
              </span>
              <div className="text-sm font-semibold text-slate-900">
                {formT.durations[data.duration]}
              </div>
            </div>
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
                {t.severity}
              </span>
              <div className="text-sm font-semibold text-slate-900">
                {data.severity}
              </div>
            </div>
          </div>

          <div className="border-t border-slate-200/60 pt-3">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
              {t.context}
            </span>
            <div className="text-sm text-slate-700">
              {data.additional_context || (
                <span className="italic text-slate-400">{t.none}</span>
              )}
            </div>
          </div>
        </div>

        {/* Safety Invariant Reminder */}
        <div className="mb-8 p-3.5 rounded-xl bg-teal-50/60 border border-teal-200 text-teal-900 text-xs flex items-center gap-2.5">
          <ShieldAlert className="w-4 h-4 text-teal-700 shrink-0" />
          <span>
            {language === 'ta'
              ? 'மதிப்பீடு உடனடியாக எங்கள் பாதுகாப்பு விதிகளால் ஆராயப்படும். அவசர எச்சரிக்கைகளுக்கு முழு முன்னுரிமை வழங்கப்படும்.'
              : 'Our deterministic safety engine will inspect this input for emergency warning signs first.'}
          </span>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <button
            type="button"
            onClick={onEdit}
            disabled={isLoading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl border border-slate-300 text-slate-700 text-sm font-semibold hover:bg-slate-50 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>{t.backToEdit}</span>
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={isLoading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-teal-700 hover:bg-teal-800 disabled:bg-slate-400 text-white text-sm font-bold shadow-sm transition transform hover:-translate-y-0.5"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>
                  {language === 'ta' ? 'மதிப்பிடப்படுகிறது...' : 'Analyzing safely...'}
                </span>
              </>
            ) : (
              <>
                <CheckCircle2 className="w-4 h-4" />
                <span>{t.confirmAndAnalyze}</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
