# HealthGuide AI — Safety & Functional Test Plan

This document details the test strategy, verification matrix, and automated test execution report for HealthGuide AI.

---

## 1. Test Strategy Overview
Safety-critical healthcare software requires rigorous deterministic verification. In accordance with clinical software engineering principles, automated unit and integration tests are executed across five critical domains:

1. **Deterministic Red-Flag Detection:** Guaranteeing zero false negatives on acute emergency warning signs.
2. **Safety Priority Invariant:** Verifying that emergency classifications cannot be downgraded by LLMs or user selections.
3. **Curated Educational Integrity:** Ensuring absence of fabricated probabilities, fake diagnoses, or dosage recommendations.
4. **Bilingual Correctness:** Confirming semantic and functional fidelity between English and Tamil.
5. **Data Privacy & Log Masking:** Verifying that personal health inputs never leak to persistent logs or databases.

---

## 2. Automated Test Suite (Pytest)

The test suite is located in `backend/tests/` and executes using standard pytest:

```powershell
.\backend\venv\Scripts\python -m pytest backend\tests -v
```

### Verified Test Cases (21 / 21 Passing)

| Test File | Test Function | Purpose / Safety Rule | Status |
| :--- | :--- | :--- | :--- |
| `test_health.py` | `test_health_check_endpoint` | Verifies `GET /api/health` returns healthy status and supported languages. | **PASSED** |
| `test_emergency_rules.py` | `test_chest_pain_variations` | Checks detection of acute chest pain, squeezing, radiating pain, and Tamil terms (`நெஞ்சு வலி`). | **PASSED** |
| `test_emergency_rules.py` | `test_respiratory_distress_variations` | Tests variations for asphyxiation, gasping, inability to inhale, and Tamil (`மூச்சுத் திணறல்`). | **PASSED** |
| `test_emergency_rules.py` | `test_stroke_neurological_variations` | Tests stroke FAST symptoms: facial droop, slurred speech, one-sided weakness (`பக்கவாதம்`). | **PASSED** |
| `test_emergency_rules.py` | `test_altered_consciousness_variations` | Tests syncope, unresponsive states, seizures, and sudden acute confusion (`மயக்கம்`). | **PASSED** |
| `test_emergency_rules.py` | `test_severe_bleeding_variations` | Tests vomiting blood, hemoptysis, gushing hemorrhage, and black tarry stools. | **PASSED** |
| `test_emergency_rules.py` | `test_anaphylaxis_variations` | Tests airway edema, tongue/throat swelling, and acute anaphylaxis. | **PASSED** |
| `test_emergency_rules.py` | `test_thunderclap_headache` | Tests sudden explosive headache of maximum intensity ("worst headache of life"). | **PASSED** |
| `test_emergency_rules.py` | `test_poisoning_overdose` | Tests accidental or intentional toxic chemical or medication ingestion. | **PASSED** |
| `test_emergency_rules.py` | `test_non_emergency_benign_symptoms` | Verifies benign cases (mild tension headache, simple sneeze) do NOT trigger false alarms. | **PASSED** |
| `test_safety_priority.py` | `test_emergency_overrides_mild_severity_selection` | Verifies that emergency keywords trigger EMERGENCY even if user selects "MILD" severity. | **PASSED** |
| `test_safety_priority.py` | `test_ai_service_emergency_bypass_guarantee` | Confirms AI processing is completely bypassed when an emergency is detected. | **PASSED** |
| `test_safety_priority.py` | `test_ai_unavailable_fallback` | Verifies smooth deterministic fallback when no AI keys or external network are present. | **PASSED** |
| `test_api_assess.py` | `test_valid_routine_symptom_assessment` | Validates complete assessment response structure, trusted sources, and disclaimers. | **PASSED** |
| `test_api_assess.py` | `test_empty_and_whitespace_symptoms_rejected` | Confirms Pydantic input validation blocks empty and whitespace-only payloads (HTTP 422). | **PASSED** |
| `test_api_assess.py` | `test_excessively_long_symptoms_rejected` | Confirms payloads over 1500 characters are blocked to prevent buffer or injection risks. | **PASSED** |
| `test_api_assess.py` | `test_invalid_age_range_rejected` | Verifies invalid enum strings are rejected safely. | **PASSED** |
| `test_api_assess.py` | `test_ambiguous_symptoms_handling` | Confirms atypical symptoms result in clinician referral without inventing diagnoses. | **PASSED** |
| `test_translations.py` | `test_tamil_emergency_assessment` | Verifies Tamil emergency triage produces accurate localized hotlines and next steps. | **PASSED** |
| `test_translations.py` | `test_tamil_routine_curated_assessment` | Confirms routine symptoms in Tamil yield appropriate curated guidance and self-care. | **PASSED** |
| `test_privacy_logging.py` | `test_privacy_no_raw_symptom_logging` | Asserts that patient symptom descriptions are masked and never written to server logs. | **PASSED** |

---

## 3. Manual Functional Checklist

- [x] **Top Navigation:** Brand logo, navigation anchors, MVP tag, and language toggle function seamlessly.
- [x] **Hero Section:** Clear value proposition, tagline, and instant "Start Symptom Check" anchor.
- [x] **Emergency Priority Banner:** Universal emergency numbers visible on top banner.
- [x] **Fictional Demo Presets:** 3 fictional scenarios (Emergency, Routine, Ambiguous) load into form with 1 click.
- [x] **Form Validation:** Character counter (3 - 1500 chars), age bracket radio pills, severity cards, and duration selection.
- [x] **Two-Step Verification:** Review step displays entered information and allows editing before submitting.
- [x] **Urgency Tiers:** Visual color-coded cards for EMERGENCY (Red), SEEK CARE SOON (Amber), SELF CARE (Teal), and AMBIGUOUS (Slate).
- [x] **Clickable Medical Citations:** Direct external links to MedlinePlus and NHS with relevance descriptions.
- [x] **Print / Save Option:** Triggers clean browser print preview of assessment summary.
- [x] **Zero Persistence:** No cookies, no authentication, no database tables.
