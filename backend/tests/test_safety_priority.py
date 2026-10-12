import pytest
from starlette.testclient import TestClient
from backend.app.models import SymptomAssessmentRequest, AgeRange, DurationCategory, SeverityLevel, LanguageChoice
from backend.app.services.ai_service import AIService


def test_emergency_overrides_mild_severity_selection(client: TestClient):
    # Even if user selects "MILD", presence of chest pain MUST trigger EMERGENCY
    payload = {
        "age_range": "ADULT_18_64",
        "symptoms_text": "I feel crushing chest pain radiating to left arm",
        "duration": "LESS_THAN_24_HOURS",
        "severity": "MILD",
        "language": "en",
    }
    response = client.post("/api/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency_level"] == "EMERGENCY"
    assert data["is_emergency"] is True
    assert data["emergency_notice"] is not None
    assert "911" in str(data["emergency_notice"]["emergency_numbers"])
    # Self-care advice MUST be empty to avoid dangerous delays
    assert len(data["self_care_guidance"]) == 0


@pytest.mark.asyncio
async def test_ai_service_emergency_bypass_guarantee():
    ai_service = AIService()
    req = SymptomAssessmentRequest(
        age_range=AgeRange.ADULT_18_64,
        symptoms_text="Severe sudden shortness of breath and turning blue",
        duration=DurationCategory.LESS_THAN_24_HOURS,
        severity=SeverityLevel.CRITICAL,
        language=LanguageChoice.EN,
    )
    res = await ai_service.assess(req)
    assert res.urgency_level.value == "EMERGENCY"
    assert res.is_emergency is True
    assert res.engine_source == "deterministic_safety_engine"


@pytest.mark.asyncio
async def test_ai_unavailable_fallback():
    # When no AI keys configured, engine must gracefully deliver deterministic assessment
    ai_service = AIService()
    req = SymptomAssessmentRequest(
        age_range=AgeRange.ADULT_18_64,
        symptoms_text="Running nose, mild sore throat, and sneezing for 3 days",
        duration=DurationCategory.DAYS_1_TO_3,
        severity=SeverityLevel.MILD,
        language=LanguageChoice.EN,
    )
    res = await ai_service.assess(req)
    assert res.urgency_level.value == "SELF_CARE_MONITOR"
    assert res.engine_source == "deterministic_safety_engine"
    assert len(res.possible_explanations) > 0
    assert len(res.self_care_guidance) > 0
