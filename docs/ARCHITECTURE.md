# HealthGuide AI — System Architecture & Data Flow

This document details the software architecture, safety triage pipeline, and data flow of **HealthGuide AI**.

---

## 1. High-Level Architecture Overview

HealthGuide AI utilizes a modern, decoupled client-server architecture built for reliability, deterministic safety, and zero data persistence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND CLIENT (Browser)                       │
│    React 18 • TypeScript • Tailwind CSS • Lucide Icons • Vite          │
│                                                                        │
│  [Hero & Emergency Banner]  [Bilingual i18n Engine (EN / தமிழ்)]        │
│  [Guided Intake Form]       [Pre-Submission Review Step]               │
│  [Results Dashboard]        [Fictional Demo Presets]                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (Proxy /api)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND SERVER (FastAPI)                        │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 1. Privacy-Preserving Middleware                                 │  │
│  │    • Sanitizes and masks health text in server access logs       │  │
│  │    • CORS & Security Headers                                     │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 2. Pydantic Input Validation                                     │  │
│  │    • AgeRange, DurationCategory, SeverityLevel enums             │  │
│  │    • Character limits: 3 <= len(symptoms_text) <= 1500           │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 3. Deterministic Safety Engine (detector.py & triage.py)         │  │
│  │    • Scans Curated Emergency Rules (Regex & Tamil Lexicon)       │  │
│  │    • CHEST, BREATHING, STROKE, CONSCIOUSNESS, BLEEDING, ANAPHYL  │  │
│  └──────┬────────────────────────────────────────────────────┬──────┘  │
│         │                                                    │         │
│  [EMERGENCY DETECTED]                                [NO RED FLAG]     │
│         │                                                    │         │
│         ▼                                                    ▼         │
│  ┌───────────────────────────────┐           ┌──────────────────────┐  │
│  │ ZERO-DOWNGRADE INVARIANT      │           │ Curated Knowledge    │  │
│  │ • Assign EMERGENCY tier       │           │ Pattern Matching     │  │
│  │ • Bypass LLM / external API   │           │ (Headache, Cold,     │  │
│  │ • Suppress self-care advice   │           │ Indigestion, etc.)   │  │
│  │ • Surface direct hotlines     │           └──────────┬───────────┘  │
│  └──────────────┬────────────────┘                      │              │
│                 │                             [OPTIONAL AI SERVICE]    │
│                 │                             (Gemini/OpenAI if keyed; │
│                 │                              deterministic fallback) │
│                 │                                       │              │
│                 └───────────────────┬───────────────────┘              │
│                                     ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 4. Structured Assessment Response (AssessmentResponse Model)     │  │
│  │    • Urgency level & emergency notice                            │  │
│  │    • Observed signals & vetted explanations (NO fake stats)      │  │
│  │    • Low-risk self-care (if non-emergency)                       │  │
│  │    • Actionable next steps & MedlinePlus / NHS citations         │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Modules & Responsibilities

### Frontend (`frontend/src/`)
- `components/Header.tsx`: Brand navigation with instant language switcher (EN / தமிழ்) and emergency quick-dial badge.
- `components/Hero.tsx`: Communicates value proposition and educational purpose.
- `components/EmergencyBanner.tsx`: High-visibility emergency warning strip with 112 / 108 / 911 quick actions.
- `components/DemoPresets.tsx`: 3 fictional scenarios (Emergency, Routine, Ambiguous) for rapid demonstration.
- `components/SymptomIntakeForm.tsx`: Collects non-identifiable health parameters (age category, symptoms, duration, severity, context).
- `components/ReviewStep.tsx`: Gives users an explicit review and confirmation step prior to assessment submission.
- `components/AssessmentResult.tsx`: Renders tiered urgency banners, emergency notices, curated explanations, and clickable MedlinePlus/NHS citations.
- `i18n/translations.ts`: Centralized, reviewed static translations for English and Tamil.
- `services/api.ts`: Typed Fetch API client with timeout protection and robust error extraction.

### Backend (`backend/app/`)
- `main.py`: FastAPI application routing `GET /api/health` and `POST /api/assess` with privacy middleware and validation error handling.
- `config.py`: Environment configuration via Pydantic model reading `.env` (ports, CORS origins, optional AI keys).
- `models.py`: Strongly-typed Pydantic models for request payloads and structured assessment responses.
- `safety/rules.py`: Curated, audited dictionary of emergency warning signs and conservative regular expressions with English and Tamil variations.
- `safety/detector.py`: Scans normalized text against compiled patterns to extract red-flag matches.
- `safety/triage.py`: Executes deterministic triage, enforces the Zero-Downgrade Invariant, and maps non-emergency cases to educational guidance.
- `services/curated_knowledge.py`: Curated medical knowledge base for common symptom clusters and verified URLs to MedlinePlus and NHS.
- `services/ai_service.py`: Optional hybrid provider (Gemini / OpenAI) with server-side secrets, rigorous prompt guardrails, and instant deterministic fallback.

---

## 3. Data Flow & Security Principles

1. **Zero Database Persistence:**  
   HealthGuide AI contains no database connection strings or tables. Inquiries are processed entirely in memory.
2. **Privacy-Masked Logging:**  
   Access logging middleware logs only sanitized HTTP metadata (HTTP method, path, response code, duration). User symptom text is excluded from all server logs.
3. **No Sensitive Query Parameters:**  
   All health data transfers occur over HTTP POST request bodies; never in query strings or URLs.
4. **Offline Capability:**  
   The entire application operates with zero external API dependencies using the built-in deterministic safety engine.
