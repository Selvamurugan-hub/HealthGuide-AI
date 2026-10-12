import React, { useState, useEffect } from 'react';
import {
  AssessmentResponse,
  LanguageChoice,
  SymptomAssessmentRequest,
} from './types';
import { checkHealth, assessSymptoms } from './services/api';
import { Header } from './components/Header';
import { EmergencyBanner } from './components/EmergencyBanner';
import { Hero } from './components/Hero';
import { SafetyNotice } from './components/SafetyNotice';
import { DemoPresets } from './components/DemoPresets';
import { SymptomIntakeForm } from './components/SymptomIntakeForm';
import { ReviewStep } from './components/ReviewStep';
import { AssessmentResult } from './components/AssessmentResult';
import { HowItWorks } from './components/HowItWorks';
import { TrustedSources } from './components/TrustedSources';
import { PrivacyNotice } from './components/PrivacyNotice';
import { Footer } from './components/Footer';

export const App: React.FC = () => {
  const [language, setLanguage] = useState<LanguageChoice>('en');
  const [stage, setStage] = useState<'FORM' | 'REVIEW' | 'RESULT'>('FORM');
  const [formData, setFormData] = useState<SymptomAssessmentRequest | null>(null);
  const [assessmentResult, setAssessmentResult] = useState<AssessmentResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<string>('checking');

  // Verify backend connection on initial load
  useEffect(() => {
    checkHealth()
      .then((h) => setBackendStatus(h.status))
      .catch(() => setBackendStatus('offline'));
  }, []);

  const handleLanguageChange = (newLang: LanguageChoice) => {
    setLanguage(newLang);
    if (formData) {
      setFormData({ ...formData, language: newLang });
    }
  };

  const handleNavigate = (sectionId: string) => {
    if (sectionId === 'home') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  const handleStartSymptomCheck = () => {
    const el = document.getElementById('intake-form');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSelectPreset = (preset: SymptomAssessmentRequest) => {
    setFormData(preset);
    setStage('FORM');
    setApiError(null);
    const el = document.getElementById('intake-form');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleProceedToReview = (data: SymptomAssessmentRequest) => {
    setFormData(data);
    setStage('REVIEW');
    setApiError(null);
    window.scrollTo({ top: 350, behavior: 'smooth' });
  };

  const handleConfirmAndAssess = async () => {
    if (!formData) return;
    setIsLoading(true);
    setApiError(null);

    try {
      const res = await assessSymptoms(formData);
      setAssessmentResult(res);
      setStage('RESULT');
      window.scrollTo({ top: 200, behavior: 'smooth' });
    } catch (err: any) {
      setApiError(err.message || 'Failed to complete assessment. Please ensure the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetForm = () => {
    setStage('FORM');
    setAssessmentResult(null);
    setFormData(null);
    setApiError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleEditSubmission = () => {
    setStage('FORM');
    setApiError(null);
    window.scrollTo({ top: 350, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
      {/* 1. Universal Emergency Banner */}
      <EmergencyBanner language={language} />

      {/* 2. Header & Navigation */}
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        onNavigate={handleNavigate}
      />

      <main className="grow">
        {/* 3. Hero Section */}
        <Hero
          language={language}
          onStartClick={handleStartSymptomCheck}
          onLearnMoreClick={() => handleNavigate('how-it-works')}
        />

        {/* Backend Status Indicator */}
        {backendStatus === 'offline' && (
          <div className="max-w-4xl mx-auto px-4 sm:px-6 my-2">
            <div className="p-3 rounded-xl bg-amber-50 border border-amber-300 text-amber-900 text-xs flex items-center justify-between">
              <span>
                Backend server is currently unreachable. Make sure the FastAPI backend is running on <code>http://127.0.0.1:8000</code>.
              </span>
            </div>
          </div>
        )}

        {/* 4. Safety Notice Box */}
        <SafetyNotice language={language} />

        {/* Global Error Notice if API issues */}
        {apiError && (
          <div className="max-w-4xl mx-auto px-4 sm:px-6 my-4">
            <div className="p-4 rounded-xl bg-rose-50 border border-rose-300 text-rose-800 text-sm flex items-center justify-between">
              <div>
                <span className="font-bold">Error: </span>
                {apiError}
              </div>
              <button
                onClick={() => setApiError(null)}
                className="text-xs font-bold uppercase underline ml-3"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* 5. Demo Presets (for judges & fictional testing) */}
        {stage === 'FORM' && (
          <DemoPresets
            language={language}
            onSelectPreset={handleSelectPreset}
          />
        )}

        {/* 6. Guided Intake Form Stage */}
        {stage === 'FORM' && (
          <SymptomIntakeForm
            language={language}
            initialValues={formData}
            onProceedToReview={handleProceedToReview}
          />
        )}

        {/* 7. Review Step Stage */}
        {stage === 'REVIEW' && formData && (
          <ReviewStep
            language={language}
            data={formData}
            isLoading={isLoading}
            onEdit={handleEditSubmission}
            onConfirm={handleConfirmAndAssess}
          />
        )}

        {/* 8. Results Dashboard Stage */}
        {stage === 'RESULT' && assessmentResult && (
          <AssessmentResult
            language={language}
            result={assessmentResult}
            onReset={handleResetForm}
            onEdit={handleEditSubmission}
          />
        )}

        {/* 9. Educational Background & Principles */}
        <HowItWorks language={language} />

        {/* 10. Trusted Public Health Sources */}
        <TrustedSources language={language} />

        {/* 11. Privacy & Limitations */}
        <PrivacyNotice language={language} />
      </main>

      {/* 12. Footer */}
      <Footer language={language} />
    </div>
  );
};

export default App;
