# HealthGuide AI — Project Description
**Tagline:** Understand symptoms. Recognize warning signs. Take safer next steps.  
**Track:** UnivaBio 2026 Hackathon — Healthcare & Safety-Focused AI  
**Repository:** Selvamurugan-hub/dell / HealthGuide AI  

---

## 1. Executive Summary
Patients and individuals encountering acute or unfamiliar health symptoms often turn to unverified internet search results or hallucination-prone conversational chatbots. These existing tools frequently introduce two catastrophic failure modes:
1. **False reassurance:** Underplaying dangerous red-flag signs (such as acute chest tightness, stroke symptoms, or severe anaphylaxis), which delays life-saving emergency medical interventions.
2. **Fabricated anxiety:** Inventing arbitrary illness likelihoods, specious disease diagnoses, or statistical probabilities that have no medical basis.

**HealthGuide AI** solves this critical problem through an auditable, deterministic, safety-first health information system. It bridges the gap between patient uncertainty and clinical care by providing accessible, bilingual (English & Tamil) educational health information, immediate red-flag emergency screening, and clear guidance on when and how to seek professional clinical care.

**Crucial Mandate:** HealthGuide AI is strictly an educational prototype and **not a diagnostic tool**. It never diagnoses disease, calculates fabricated confidence scores, prescribes dosages, or replaces a licensed clinician.

---

## 2. Key Capabilities & Innovations

- **Deterministic Safety-First Triage Engine:**  
  Input is scanned against a curated clinical ruleset of acute emergency warning signs (cardiovascular distress, severe respiratory compromise, FAST stroke symptoms, altered mental status, severe hemorrhaging, and anaphylaxis) **prior to any optional AI analysis**.
- **The Zero-Downgrade Safety Invariant:**  
  If a red-flag condition is detected, an emergency alert is triggered immediately with universal hotline links (112 / 108 / 911 / 999). No downstream LLM or user selection is ever permitted to suppress, downplay, or downgrade an emergency warning.
- **Vetted Curated Knowledge vs. AI Hallucination:**  
  Common non-emergency symptom patterns (e.g., tension headaches, upper respiratory viral infections, mild dyspepsia) map to verified public health guidance from **MedlinePlus** and the **NHS**. The application completely eliminates fabricated statistics and clinical percentages.
- **Accessible Bilingual Support (English & தமிழ்):**  
  Full natural language localization across interfaces, triage rules, emergency hotlines, and educational explanations, ensuring linguistic equity and accessibility.
- **Privacy by Design & Zero Health Persistence:**  
  No logins, no cookies, no tracking. Health inputs are processed strictly in-memory and are never stored in a database. Server logs actively sanitize and mask health descriptions to prevent data leakage.
- **Rapid Fictional Demo Presets:**  
  Allows judges and developers to test emergency priority, routine self-care, and ambiguous presentation pathways in one click without entering personal health information.

---

## 3. Technology Stack

- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons.
- **Backend:** Python 3.9+, FastAPI, Pydantic v2, Uvicorn.
- **Testing:** Pytest, Starlette TestClient (21 automated safety, translation, and privacy tests).
- **Architecture:** Decoupled RESTful API with deterministic rule-engine core and optional guarded server-side AI fallback.

---

## 4. Safety Disclaimer
HealthGuide AI is developed strictly for research, educational, and hackathon evaluation purposes. It is not clinically certified as a medical device. Anyone experiencing sudden, severe, or life-threatening symptoms must immediately contact their local emergency services.
