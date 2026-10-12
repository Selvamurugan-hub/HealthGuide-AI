import React, { useState } from 'react';
import {
  AlertCircle,
  Clock,
  HelpCircle,
  Lock,
  Send,
  User,
  Zap,
} from 'lucide-react';
import {
  AgeRange,
  DurationCategory,
  LanguageChoice,
  SeverityLevel,
  SymptomAssessmentRequest,
} from '../types';
import { translations } from '../i18n/translations';

interface SymptomIntakeFormProps {
  language: LanguageChoice;
  initialValues?: SymptomAssessmentRequest | null;
  onProceedToReview: (data: SymptomAssessmentRequest) => void;
}

export const SymptomIntakeForm: React.FC<SymptomIntakeFormProps> = ({
  language,
  initialValues,
  onProceedToReview,
}) => {
  const t = translations[language].form;

  const [ageRange, setAgeRange] = useState<AgeRange>(
    initialValues?.age_range || 'ADULT_18_64'
  );
  const [symptomsText, setSymptomsText] = useState<string>(
    initialValues?.symptoms_text || ''
  );
  const [duration, setDuration] = useState<DurationCategory>(
    initialValues?.duration || 'DAYS_1_TO_3'
  );
  const [severity, setSeverity] = useState<SeverityLevel>(
    initialValues?.severity || 'MILD'
  );
  const [additionalContext, setAdditionalContext] = useState<string>(
    initialValues?.additional_context || ''
  );
  const [validationError, setValidationError] = useState<string | null>(null);

  // Update when preset is loaded
  React.useEffect(() => {
    if (initialValues) {
      setAgeRange(initialValues.age_range);
      setSymptomsText(initialValues.symptoms_text);
      setDuration(initialValues.duration);
      setSeverity(initialValues.severity);
      setAdditionalContext(initialValues.additional_context || '');
      setValidationError(null);
    }
  }, [initialValues]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const cleanSymptoms = symptomsText.trim();

    if (cleanSymptoms.length < 3) {
      setValidationError(
        language === 'ta'
          ? 'தயவுசெய்து குறைந்தது 3 எழுத்துக்களில் உங்கள் அறிகுறிகளை விவரிக்கவும்.'
          : 'Please enter at least 3 characters describing what symptoms you are experiencing.'
      );
      return;
    }

    if (cleanSymptoms.length > 1500) {
      setValidationError(
        language === 'ta'
          ? 'அறிகுறி விளக்கம் 1500 எழுத்துக்களுக்கு மிகாமல் இருக்க வேண்டும்.'
          : 'Symptom description must not exceed 1500 characters.'
      );
      return;
    }

    setValidationError(null);
    onProceedToReview({
      age_range: ageRange,
      symptoms_text: cleanSymptoms,
      duration,
      severity,
      additional_context: additionalContext.trim() || undefined,
      language,
    });
  };

  return (
    <div id="intake-form" className="max-w-4xl mx-auto px-4 sm:px-6 my-8">
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 sm:p-8 shadow-sm">
        <div className="border-b border-slate-100 pb-5 mb-6">
          <div className="flex items-center gap-2 text-teal-700 text-xs font-bold uppercase tracking-wider mb-1">
            <span className="w-2 h-2 rounded-full bg-teal-600 animate-pulse"></span>
            {t.step1Title}
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            {language === 'ta'
              ? 'அறிகுறி வழிகாட்டல் படிவம்'
              : 'Guided Symptom Intake'}
          </h2>
        </div>

        {validationError && (
          <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3 text-rose-800 text-sm animate-shake">
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
            <span>{validationError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-7">
          {/* 1. Age Range Selection */}
          <div>
            <label className="block text-sm font-bold text-slate-900 mb-1 flex items-center gap-1.5">
              <User className="w-4 h-4 text-teal-700" />
              {t.ageLabel} <span className="text-rose-500">*</span>
            </label>
            <p className="text-xs text-slate-500 mb-3">{t.ageHint}</p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {(
                [
                  'CHILD_0_12',
                  'TEEN_13_17',
                  'ADULT_18_64',
                  'OLDER_ADULT_65_PLUS',
                ] as AgeRange[]
              ).map((ar) => (
                <button
                  key={ar}
                  type="button"
                  onClick={() => setAgeRange(ar)}
                  className={`p-3 rounded-xl border text-left text-xs sm:text-sm font-semibold transition ${
                    ageRange === ar
                      ? 'border-teal-600 bg-teal-50/60 text-teal-900 ring-2 ring-teal-600/20'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {t.ages[ar]}
                </button>
              ))}
            </div>
          </div>

          {/* 2. Main Symptoms Textarea */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label
                htmlFor="symptoms_text"
                className="text-sm font-bold text-slate-900 flex items-center gap-1.5"
              >
                <Zap className="w-4 h-4 text-teal-700" />
                {t.symptomLabel} <span className="text-rose-500">*</span>
              </label>
              <span className="text-xs text-slate-400">
                {symptomsText.length} / 1500 {t.charCount}
              </span>
            </div>
            <textarea
              id="symptoms_text"
              rows={4}
              required
              value={symptomsText}
              onChange={(e) => setSymptomsText(e.target.value)}
              placeholder={t.symptomPlaceholder}
              className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-teal-600 focus:ring-3 focus:ring-teal-100 text-slate-800 text-sm placeholder:text-slate-400 transition outline-none resize-y"
            />
            <p className="text-xs text-slate-500 mt-1">{t.symptomMinNotice}</p>
          </div>

          {/* 3. Duration Category */}
          <div>
            <label className="block text-sm font-bold text-slate-900 mb-2 flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-teal-700" />
              {t.durationLabel} <span className="text-rose-500">*</span>
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
              {(
                [
                  'LESS_THAN_24_HOURS',
                  'DAYS_1_TO_3',
                  'DAYS_4_TO_7',
                  'WEEKS_1_TO_2',
                  'MORE_THAN_2_WEEKS',
                ] as DurationCategory[]
              ).map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => setDuration(d)}
                  className={`px-3 py-2.5 rounded-xl border text-center text-xs font-semibold transition ${
                    duration === d
                      ? 'border-teal-600 bg-teal-50 text-teal-900 ring-2 ring-teal-600/20'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {t.durations[d]}
                </button>
              ))}
            </div>
          </div>

          {/* 4. Severity Level Selection */}
          <div>
            <label className="block text-sm font-bold text-slate-900 mb-2 flex items-center gap-1.5">
              <HelpCircle className="w-4 h-4 text-teal-700" />
              {t.severityLabel} <span className="text-rose-500">*</span>
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {(
                ['MILD', 'MODERATE', 'SEVERE', 'CRITICAL'] as SeverityLevel[]
              ).map((sev) => {
                const isSelected = severity === sev;
                const badgeColor =
                  sev === 'CRITICAL'
                    ? 'text-rose-700'
                    : sev === 'SEVERE'
                    ? 'text-amber-700'
                    : sev === 'MODERATE'
                    ? 'text-blue-700'
                    : 'text-emerald-700';

                return (
                  <button
                    key={sev}
                    type="button"
                    onClick={() => setSeverity(sev)}
                    className={`p-3.5 rounded-xl border text-left text-xs sm:text-sm font-medium transition ${
                      isSelected
                        ? 'border-teal-600 bg-teal-50/70 text-slate-900 ring-2 ring-teal-600/20'
                        : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`font-bold text-xs uppercase ${badgeColor}`}>
                        {sev}
                      </span>
                      <div
                        className={`w-3.5 h-3.5 rounded-full border ${
                          isSelected
                            ? 'border-teal-600 bg-teal-600'
                            : 'border-slate-300'
                        }`}
                      />
                    </div>
                    <p className="text-xs text-slate-600 leading-normal">
                      {t.severities[sev]}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 5. Additional Context (Optional) */}
          <div>
            <label
              htmlFor="additional_context"
              className="block text-sm font-bold text-slate-900 mb-1"
            >
              {t.contextLabel}
            </label>
            <input
              id="additional_context"
              type="text"
              maxLength={1000}
              value={additionalContext}
              onChange={(e) => setAdditionalContext(e.target.value)}
              placeholder={t.contextPlaceholder}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-teal-600 focus:ring-3 focus:ring-teal-100 text-slate-800 text-sm placeholder:text-slate-400 transition outline-none"
            />
          </div>

          {/* Privacy Notice Strip */}
          <div className="flex items-center gap-2 p-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-600 text-xs">
            <Lock className="w-4 h-4 text-slate-500 shrink-0" />
            <span>{t.privacyCheck}</span>
          </div>

          {/* Form Action */}
          <div className="pt-2">
            <button
              type="submit"
              className="w-full inline-flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-bold text-base shadow-sm hover:shadow transition transform hover:-translate-y-0.5"
            >
              <Send className="w-4 h-4" />
              <span>{t.reviewBtn}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
