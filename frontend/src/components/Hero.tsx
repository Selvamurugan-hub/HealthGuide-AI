import React from 'react';
import {
  ArrowRight,
  ShieldCheck,
  HeartPulse,
  Sparkles,
  CheckCircle2,
  Activity,
  Plus,
  Stethoscope,
} from 'lucide-react';

import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface HeroProps {
  language: LanguageChoice;
  onStartClick: () => void;
  onLearnMoreClick: () => void;
}

export const Hero: React.FC<HeroProps> = ({
  language,
  onStartClick,
  onLearnMoreClick,
}) => {
  const t = translations[language].hero;

  return (
    <section className="relative isolate overflow-hidden border-b border-slate-200/70 bg-gradient-to-br from-white via-teal-50/50 to-slate-50">

      {/* Background decoration */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 -top-32 -z-10 h-96 w-96 rounded-full bg-teal-200/25 blur-3xl"
      />

      <div
        aria-hidden="true"
        className="pointer-events-none absolute -bottom-40 -left-24 -z-10 h-96 w-96 rounded-full bg-cyan-100/40 blur-3xl"
      />

      <div className="mx-auto grid max-w-7xl items-center gap-12 px-4 py-14 sm:px-6 sm:py-20 lg:grid-cols-[1.1fr_0.9fr] lg:gap-14 lg:px-8 lg:py-24">

        {/* Left: Main content */}
        <div className="hg-animate-in text-center lg:text-left">

          {/* Badge */}
          <div className="mb-7 inline-flex max-w-full items-center gap-2 rounded-full border border-teal-200/80 bg-white/85 px-3.5 py-2 text-xs font-semibold text-teal-800 shadow-sm sm:text-sm">
            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-teal-100">
              <Sparkles className="h-3.5 w-3.5 text-teal-700" />
            </span>
            <span>{t.badge}</span>
          </div>

          {/* Heading */}
          <h1 className="mx-auto mb-6 max-w-2xl text-[2.45rem] font-extrabold leading-[1.13] tracking-[-0.045em] text-slate-900 sm:text-5xl lg:mx-0 lg:text-[3.65rem] xl:text-[4rem]">
            {t.title}{' '}
            <span className="relative inline-block text-teal-700">
              {t.titleHighlight}
              <svg
                aria-hidden="true"
                viewBox="0 0 220 12"
                fill="none"
                className="absolute -bottom-2 left-0 h-2 w-full text-teal-300"
                preserveAspectRatio="none"
              >
                <path
                  d="M3 8C55 2 145 2 217 7"
                  stroke="currentColor"
                  strokeWidth="5"
                  strokeLinecap="round"
                />
              </svg>
            </span>
          </h1>

          {/* Description */}
          <p className="mx-auto mb-9 max-w-xl text-base leading-8 text-slate-600 sm:text-lg lg:mx-0">
            {t.description}
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col items-stretch justify-center gap-3 sm:flex-row sm:items-center lg:justify-start">

            <button
              type="button"
              onClick={onStartClick}
              className="hg-button-primary min-h-[54px] w-full px-6 text-sm sm:w-auto sm:text-base"
            >
              <HeartPulse className="h-5 w-5" />
              <span>{t.startBtn}</span>
              <ArrowRight className="ml-1 h-4 w-4 transition-transform duration-200 group-hover:translate-x-1" />
            </button>

            <button
              type="button"
              onClick={onLearnMoreClick}
              className="inline-flex min-h-[54px] w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/90 px-6 text-sm font-semibold text-slate-700 shadow-sm transition duration-200 hover:border-teal-200 hover:bg-teal-50/70 hover:text-teal-800 sm:w-auto sm:text-base"
            >
              <ShieldCheck className="h-5 w-5 text-teal-700" />
              <span>{t.learnMoreBtn}</span>
            </button>
          </div>

          {/* Trust indicators */}
          <div className="mt-9 flex flex-wrap items-center justify-center gap-x-5 gap-y-3 text-xs font-medium text-slate-500 sm:gap-x-6 lg:justify-start">
            <div className="inline-flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-teal-600" />
              <span>Safety-first guidance</span>
            </div>

            <div className="inline-flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-teal-600" />
              <span>Educational, not diagnostic</span>
            </div>
          </div>
        </div>

        {/* Right: Healthcare visual */}
        <div className="relative mx-auto w-full max-w-md lg:max-w-none">

          {/* Decorative rings */}
          <div
            aria-hidden="true"
            className="absolute left-1/2 top-1/2 h-[320px] w-[320px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-teal-200/60 sm:h-[390px] sm:w-[390px]"
          />

          <div
            aria-hidden="true"
            className="absolute left-1/2 top-1/2 h-[265px] w-[265px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-dashed border-teal-200/70 sm:h-[330px] sm:w-[330px]"
          />

          {/* Main visual card */}
          <div className="relative mx-auto max-w-[370px] rounded-[30px] border border-white bg-white/90 p-5 shadow-[0_24px_80px_-24px_rgba(15,118,110,0.22)] backdrop-blur-sm sm:p-7">

            {/* Card heading */}
            <div className="mb-7 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-teal-700">
                  HealthGuide AI
                </p>
                <h2 className="mt-1 text-lg font-bold tracking-tight text-slate-900">
                  Your health, understood.
                </h2>
              </div>

              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">
                <Activity className="h-6 w-6" />
              </div>
            </div>

            {/* Main shield illustration */}
            <div className="relative mb-7 flex h-[190px] items-center justify-center overflow-hidden rounded-[24px] bg-gradient-to-br from-teal-50 via-cyan-50/70 to-emerald-50">

              <div
                aria-hidden="true"
                className="absolute h-36 w-36 rounded-full bg-white/80 shadow-inner"
              />

              <div className="relative flex h-28 w-28 items-center justify-center rounded-[30px] bg-gradient-to-br from-teal-500 to-teal-700 text-white shadow-xl shadow-teal-700/20">
                <ShieldCheck
                  className="h-[68px] w-[68px]"
                  strokeWidth={1.35}
                />

                <div className="absolute inset-0 flex items-center justify-center">
                  <Plus
                    className="h-8 w-8 text-white"
                    strokeWidth={3}
                  />
                </div>
              </div>

              {/* Floating activity icon */}
              <div className="absolute right-7 top-7 flex h-11 w-11 items-center justify-center rounded-2xl border border-white bg-white text-teal-700 shadow-md">
                <HeartPulse className="h-5 w-5" />
              </div>

              {/* Floating stethoscope icon */}
              <div className="absolute bottom-6 left-6 flex h-11 w-11 items-center justify-center rounded-2xl border border-white bg-white text-teal-700 shadow-md">
                <Stethoscope className="h-5 w-5" />
              </div>

              <div className="absolute bottom-5 right-6 h-3 w-3 rounded-full bg-emerald-400 ring-4 ring-white/80" />
            </div>

            {/* Information cards */}
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-slate-100 bg-slate-50/90 p-3.5">
                <div className="mb-2 flex h-8 w-8 items-center justify-center rounded-xl bg-teal-100 text-teal-700">
                  <Activity className="h-4 w-4" />
                </div>

                <p className="text-xs font-bold text-slate-800">
                  Symptom guidance
                </p>
                <p className="mt-1 text-[11px] leading-5 text-slate-500">
                  Understand possible next steps
                </p>
              </div>

              <div className="rounded-2xl border border-slate-100 bg-slate-50/90 p-3.5">
                <div className="mb-2 flex h-8 w-8 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
                  <ShieldCheck className="h-4 w-4" />
                </div>

                <p className="text-xs font-bold text-slate-800">
                  Safety awareness
                </p>
                <p className="mt-1 text-[11px] leading-5 text-slate-500">
                  Recognize warning signs
                </p>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="mt-4 flex items-start gap-2.5 rounded-xl border border-amber-100 bg-amber-50/80 p-3">
              <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-amber-700" />

              <p className="text-[10px] leading-5 text-amber-900 sm:text-[11px]">
                For health education only. Not a medical diagnosis or a substitute for professional care.
              </p>
            </div>
          </div>

          {/* Floating accent */}
          <div
            aria-hidden="true"
            className="absolute -right-2 top-12 -z-10 h-16 w-16 rounded-2xl bg-teal-200/50 blur-xl sm:-right-4"
          />

          <div
            aria-hidden="true"
            className="absolute -bottom-4 left-8 -z-10 h-20 w-20 rounded-full bg-cyan-200/40 blur-2xl"
          />
        </div>
      </div>
    </section>
  );
};

export default Hero;