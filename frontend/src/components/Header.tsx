import React, { useState } from 'react';
import {
  Activity,
  Globe,
  PhoneCall,
  ShieldCheck,
  Menu,
  X,
  ArrowUpRight,
} from 'lucide-react';

import { LanguageChoice } from '../types';
import { translations } from '../i18n/translations';

interface HeaderProps {
  language: LanguageChoice;
  onLanguageChange: (lang: LanguageChoice) => void;
  onNavigate: (sectionId: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  language,
  onLanguageChange,
  onNavigate,
}) => {
  const t = translations[language].nav;
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigateTo = (sectionId: string) => {
    onNavigate(sectionId);
    setMobileMenuOpen(false);
  };

  const navItems = [
    { label: t.home, section: 'home' },
    { label: t.howItWorks, section: 'how-it-works' },
    { label: t.sources, section: 'sources' },
    { label: t.privacy, section: 'privacy' },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/70 bg-white/90 backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-[72px] items-center justify-between gap-3 md:h-20">

          {/* Brand */}
          <button
            type="button"
            onClick={() => navigateTo('home')}
            aria-label={`${t.appName} - Home`}
            className="group flex min-w-0 items-center gap-3 rounded-xl text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-4"
          >
            {/* Brand icon */}
            <div className="relative flex h-11 w-11 shrink-0 items-center justify-center rounded-[15px] bg-gradient-to-br from-teal-500 to-teal-700 text-white shadow-lg shadow-teal-700/15 transition duration-300 group-hover:-translate-y-0.5 group-hover:shadow-teal-700/25 sm:h-12 sm:w-12">
              <ShieldCheck
                className="h-6 w-6 sm:h-7 sm:w-7"
                strokeWidth={1.9}
              />

              <span className="absolute -bottom-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full border-2 border-white bg-emerald-400">
                <Activity className="h-2 w-2 text-white" />
              </span>
            </div>

            {/* Brand text */}
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className="truncate font-extrabold text-[17px] tracking-tight text-slate-900 sm:text-xl">
                  {t.appName}
                </span>

                <span className="hidden rounded-full border border-teal-100 bg-teal-50 px-2 py-0.5 text-[9px] font-bold uppercase tracking-[0.12em] text-teal-700 sm:inline-flex">
                  AI
                </span>
              </div>

              <p className="mt-0.5 hidden max-w-[240px] truncate text-[11px] font-medium tracking-wide text-slate-500 sm:block">
                {t.tagline}
              </p>
            </div>
          </button>

          {/* Desktop navigation */}
          <nav
            aria-label="Main navigation"
            className="hidden items-center gap-1 lg:flex"
          >
            {navItems.map((item) => (
              <button
                key={item.section}
                type="button"
                onClick={() => navigateTo(item.section)}
                className="rounded-xl px-3 py-2.5 text-[13px] font-semibold text-slate-600 transition duration-200 hover:bg-teal-50 hover:text-teal-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 xl:px-4"
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Right actions */}
          <div className="flex shrink-0 items-center gap-2 sm:gap-3">

            {/* Emergency information */}
            <div
              className="hidden items-center gap-2 rounded-xl border border-rose-100 bg-rose-50/80 px-3 py-2 xl:flex"
              title={t.emergencyNotice}
            >
              <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-white text-rose-600 shadow-sm">
                <PhoneCall className="h-3.5 w-3.5" />
              </span>

              <div>
                <p className="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                  Emergency
                </p>
                <p className="text-xs font-bold text-rose-800">
                  {t.emergencyNotice}
                </p>
              </div>
            </div>

            {/* Language selector */}
            <div
              role="group"
              aria-label="Select language"
              className="flex items-center rounded-xl border border-slate-200 bg-slate-50 p-1"
            >
              <Globe className="ml-1 mr-1 h-3.5 w-3.5 text-slate-500 sm:ml-2 sm:mr-1.5" />

              <button
                type="button"
                onClick={() => onLanguageChange('en')}
                aria-pressed={language === 'en'}
                className={`rounded-lg px-2 py-1.5 text-[11px] font-bold transition-all duration-200 sm:px-3 ${
                  language === 'en'
                    ? 'bg-white text-teal-800 shadow-sm ring-1 ring-slate-200/70'
                    : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                EN
              </button>

              <button
                type="button"
                onClick={() => onLanguageChange('ta')}
                aria-pressed={language === 'ta'}
                className={`rounded-lg px-2 py-1.5 text-[11px] font-bold transition-all duration-200 sm:px-3 ${
                  language === 'ta'
                    ? 'bg-white text-teal-800 shadow-sm ring-1 ring-slate-200/70'
                    : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                தமிழ்
              </button>
            </div>

            {/* Mobile menu toggle */}
            <button
              type="button"
              onClick={() => setMobileMenuOpen((open) => !open)}
              aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-navigation"
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 transition hover:border-teal-200 hover:bg-teal-50 hover:text-teal-800 lg:hidden"
            >
              {mobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile navigation */}
        {mobileMenuOpen && (
          <div
            id="mobile-navigation"
            className="border-t border-slate-100 py-3 lg:hidden"
          >
            <nav
              aria-label="Mobile navigation"
              className="grid gap-1"
            >
              {navItems.map((item) => (
                <button
                  key={item.section}
                  type="button"
                  onClick={() => navigateTo(item.section)}
                  className="flex items-center justify-between rounded-xl px-4 py-3 text-left text-sm font-semibold text-slate-700 transition hover:bg-teal-50 hover:text-teal-800"
                >
                  {item.label}
                  <ArrowUpRight className="h-4 w-4 text-slate-400" />
                </button>
              ))}

              <div className="mx-2 mt-2 flex items-center gap-2 rounded-xl border border-rose-100 bg-rose-50 px-3 py-3 text-xs font-medium text-rose-800">
                <PhoneCall className="h-4 w-4 shrink-0 text-rose-600" />
                <span>{t.emergencyNotice}</span>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;