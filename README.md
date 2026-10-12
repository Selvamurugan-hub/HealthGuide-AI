# HealthGuide AI

> **Understand symptoms. Recognize warning signs. Take safer next steps.**

[![UnivaBio 2026 Hackathon](https://img.shields.io/badge/UnivaBio_2026-Hackathon_MVP-0d9488.svg)](https://github.com/Selvamurugan-hub/dell)
[![Tests Passing](https://img.shields.io/badge/Tests-21%20Passed-emerald.svg)](backend/tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Bilingual: EN & TA](https://img.shields.io/badge/Bilingual-English%20%7C%20தமிழ்-indigo.svg)](frontend/src/i18n)

HealthGuide AI is an accessible, responsive, safety-first health information prototype designed for the **UnivaBio 2026 Hackathon**. It helps users describe symptoms in their own words, recognize potential emergency warning signs immediately, and understand when and how to seek professional clinical care.

> [!IMPORTANT]
> **Safety Notice:** HealthGuide AI is strictly an **educational prototype** and **NOT a diagnostic tool**. It never claims to diagnose diseases, calculate disease probabilities, recommend prescription medications, guarantee safety, or replace a licensed medical clinician.

---

## 1. Problem Statement
When individuals feel unwell, they often turn to unverified internet searches or LLM chatbots. These solutions present dangerous clinical failure modes:
1. **False Reassurance & Critical Delays:** AI models can downplay or misinterpret emergency signs (such as acute chest pain, stroke symptoms, or severe allergic reactions), delaying life-saving emergency care.
2. **Fabricated Uncertainty & Hallucinations:** Commercial AI models frequently invent disease probabilities (e.g., "78% chance of condition X") or generate fabricated citations that alarm users without clinical grounds.
3. **Language & Privacy Barriers:** Patients from non-English speaking communities often lack immediate, vetted health triage in their primary language (such as Tamil), and existing web apps demand invasive personal health logins.

---

## 2. Proposed Solution & Target Users
**HealthGuide AI** provides an honest, auditable alternative:
- **Deterministic Emergency Priority:** Scans incoming inputs against curated emergency red flags before any optional AI processing.
- **The Zero-Downgrade Invariant:** Emergency warnings cannot be suppressed or downgraded by any language model or user severity choice.
- **Curated Educational Evidence:** Explanations and self-care tips are grounded in verified public health guidelines from **MedlinePlus** and the **NHS**. No fabricated percentages.
- **Bilingual Interface (English & தமிழ்):** Full bilingual support with reviewed, natural Tamil translations for safety-critical notices, triage questions, and emergency numbers.
- **Privacy by Design:** Zero database storage. No logins. Raw symptom descriptions are masked from all server access logs.

### Target Users
- Individuals seeking guidance on whether symptoms require emergency services, urgent care, or a routine clinic visit.
- Multilingual patients and caregivers needing health information in English or Tamil.
- Hackathon evaluators and healthcare product designers interested in safety-first AI architectures.

---

## 3. Main Features
- **Deterministic Emergency Screening:** Detects cardiovascular distress, respiratory failure, stroke FAST signs, altered consciousness, severe bleeding, anaphylaxis, and poisoning.
- **Fictional Demo Presets:** 3 one-click presets (Emergency Red Flag, Routine Discomfort, Ambiguous Presentation) for rapid, safe demonstration without entering personal data.
- **Guided 2-Step Intake:** Age bracket selection (no DOB required), symptom description with character counter, duration, severity, and optional context with an explicit **Review & Verify** step.
- **Tiered Urgency Dashboard:**
  - 🚨 **EMERGENCY:** High-priority warning with direct dials to **112, 108, 911, and 999**, immediate action checklist, and suppression of home self-care advice to prevent delays.
  - ⚠️ **SEEK CARE SOON:** Clinical evaluation recommended within 12–24 hours.
  - 🌿 **SELF-CARE & MONITOR:** Conservative, safe comfort measures (hydration, rest) for low-risk routine profiles.
  - ℹ️ **AMBIGUOUS / CONSULT CLINICIAN:** Recommends doctor examination rather than guessing.
- **Clickable Medical Citations:** Direct reference links to [MedlinePlus](https://medlineplus.gov/) and [NHS Health A to Z](https://www.nhs.uk/).
- **100% Free & Offline-Ready:** The core deterministic engine requires no paid AI API keys. An optional hybrid provider (Gemini / OpenAI) can be enabled with deterministic fallback.

---

## 4. Architecture & Data Flow

```
┌─────────────────────────────────┐
│        React 18 + Vite          │  (TypeScript, Tailwind CSS, Lucide Icons)
│  Bilingual UI (English & தமிழ்) │  Intake Form • Review Step • Results Dashboard
└────────────────┬────────────────┘
                 │ HTTP POST /api/assess
                 ▼
┌─────────────────────────────────┐
│     FastAPI Backend Server      │  (Python 3.9+, Pydantic v2)
│  Privacy Middleware (Mask Logs) │  Input validation (3 - 1500 chars)
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   Deterministic Safety Engine   │  (rules.py, detector.py, triage.py)
│   Audited Regex & Tamil Rules   │  Scans 8 Emergency Categories
└────────┬───────────────┬────────┘
         │               │
  [EMERGENCY]     [NON-EMERGENCY]
         │               │
         ▼               ▼
┌────────────────┐ ┌────────────────────────────────────────────────────────┐
│ ZERO-DOWNGRADE │ │ Curated Knowledge Base (MedlinePlus & NHS)             │
│ • EMERGENCY    │ │ + Optional Server-Side AI (Gemini / OpenAI Fallback)   │
│ • Direct 112   │ └────────────────────────────────────────────────────────┘
└────────────────┘
```

Detailed architecture diagrams and module breakdowns are available in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 5. Technology Stack
- **Frontend:** React 18, Vite 6, TypeScript 5, Tailwind CSS 3, Lucide React.
- **Backend:** Python 3.9+, FastAPI, Pydantic v2, Uvicorn, Python-dotenv.
- **Testing:** Pytest 8, Starlette TestClient (21 automated tests).
- **Environment:** Windows PowerShell, Node.js v24+, Python 3.9+.

---

## 6. Windows PowerShell Setup & Run Instructions

### Prerequisites
- Windows 10/11 with PowerShell
- Python 3.9+ (`python --version`)
- Node.js 18+ and npm (`node --version`, `npm --version`)

---

### Step 1: Clone or Navigate to the Project
```powershell
cd c:\Users\dell\Desktop\Healthguideai
```

---

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
*(No API key is required to run the full application! The deterministic engine works out-of-the-box).*

---

### Step 3: Run Backend Tests
Verify all 21 automated safety, translation, and privacy tests:
```powershell
# Run the test suite using the virtual environment
.\backend\venv\Scripts\python -m pytest backend\tests -v
```
**Expected Result:** `21 passed in 2.01s`

---

### Step 4: Start the Backend Server (Terminal 1)
Open a Windows PowerShell terminal and start the FastAPI service:
```powershell
.\backend\venv\Scripts\python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API will be available at:
- Health check: `http://127.0.0.1:8000/api/health`
- Interactive OpenAPI docs: `http://127.0.0.1:8000/docs`

---

### Step 5: Start the Frontend Application (Terminal 2)
Open a second Windows PowerShell terminal and start the Vite dev server:
```powershell
cd frontend
npm run dev
```
Open your browser and navigate to:
👉 **`http://localhost:5173`**

---

### Building for Production
To build the frontend production distribution:
```powershell
cd frontend
npm run build
```
Assets are emitted to `frontend/dist/`.

---

## 7. Automated Testing Suite

All tests can be executed with a single command:
```powershell
.\backend\venv\Scripts\python -m pytest backend\tests -v
```

The 21 automated tests verify:
1. `GET /api/health` returns healthy status and supported languages.
2. Emergency warning-sign detection across all 8 red-flag categories.
3. Alternate phrasing and conservative regex variations (e.g. "tightness in chest", "coughing up blood", "throat is closing up").
4. Priority override: emergency warning triggers even if user selects "MILD" severity.
5. Invariant enforcement: AI processing is bypassed on emergency detection.
6. Offline deterministic fallback when AI is unconfigured or unreachable.
7. Tamil localization for both emergency and routine curated guidance.
8. Pydantic validation: rejection of empty, whitespace-only, or >1500 char inputs.
9. Ambiguous symptom handling without fabricated diagnoses.
10. Privacy log auditing: verifies raw patient symptom text is never logged to stdout/files.

Full test documentation is provided in [docs/TEST_PLAN.md](docs/TEST_PLAN.md).

---

## 8. Hackathon Submission Documentation

The `docs/` folder contains dedicated assets for evaluators:
- [docs/PROJECT_DESCRIPTION.md](docs/PROJECT_DESCRIPTION.md) — Polished one-page executive summary suitable for PDF export.
- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) — Step-by-step 2–3 minute English presentation script for hackathon judging.
- [docs/TEST_PLAN.md](docs/TEST_PLAN.md) — Comprehensive safety test verification matrix.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — System architecture diagram and module documentation.

---

## 9. Safety & Data-Handling Limitations

- **Not Clinically Certified:** This software is a student hackathon MVP and has not undergone clinical trials or FDA/CE regulatory clearance.
- **Limited Curated Ruleset:** The safety ruleset covers major acute emergencies but cannot detect every possible human disease or atypical presentation.
- **No Physical Examination:** Software cannot measure vital signs, palpate organs, or interpret laboratory values.
- **Future Improvements:** Future work will integrate clinical FHIR-standard triage trees, speech-to-text intake in vernacular dialects, and offline mobile deployment.

---

## 10. License
Distributed under the MIT License. See `LICENSE` for details.
