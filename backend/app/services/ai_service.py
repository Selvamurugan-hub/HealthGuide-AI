import json
import logging
from typing import Optional
import httpx
from ..config import settings
from ..models import (
    AssessmentResponse,
    LanguageChoice,
    SymptomAssessmentRequest,
    UrgencyLevel,
)
from ..safety.triage import SafetyTriageEngine

logger = logging.getLogger("healthguide.ai")


class AIService:
    """Optional AI service supporting Gemini and OpenAI with deterministic fallback."""

    def __init__(self, triage_engine: Optional[SafetyTriageEngine] = None):
        self.triage_engine = triage_engine or SafetyTriageEngine()

    async def assess(self, request: SymptomAssessmentRequest) -> AssessmentResponse:
        # 1. ALWAYS run deterministic safety triage first!
        deterministic_result = self.triage_engine.assess(request)

        # 2. Invariant: If emergency is detected, NEVER call AI and NEVER allow LLM downgrade
        if deterministic_result.is_emergency or deterministic_result.urgency_level == UrgencyLevel.EMERGENCY:
            return deterministic_result

        # 3. If no AI provider or key configured, return verified deterministic result
        provider = settings.ai_provider.upper()
        if provider == "GEMINI" and settings.gemini_api_key:
            try:
                ai_result = await self._call_gemini(request, deterministic_result)
                if ai_result:
                    return ai_result
            except Exception as e:
                logger.warning("Gemini AI integration failed; falling back to deterministic safety engine: %s", type(e).__name__)
        elif provider == "OPENAI" and settings.openai_api_key:
            try:
                ai_result = await self._call_openai(request, deterministic_result)
                if ai_result:
                    return ai_result
            except Exception as e:
                logger.warning("OpenAI integration failed; falling back to deterministic safety engine: %s", type(e).__name__)

        # Fallback to curated deterministic engine
        return deterministic_result

    async def _call_gemini(
        self, request: SymptomAssessmentRequest, fallback: AssessmentResponse
    ) -> Optional[AssessmentResponse]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.gemini_api_key}"
        prompt = self._build_prompt(request)

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
            },
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                return None
            data = resp.json()
            raw_text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            return self._parse_and_validate_ai_json(raw_text, fallback, request.language)

    async def _call_openai(
        self, request: SymptomAssessmentRequest, fallback: AssessmentResponse
    ) -> Optional[AssessmentResponse]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        prompt = self._build_prompt(request)

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are HealthGuide AI educational engine. Strictly adhere to JSON and never diagnose.",
                },
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                return None
            data = resp.json()
            raw_text = data["choices"][0]["message"]["content"]
            return self._parse_and_validate_ai_json(raw_text, fallback, request.language)

    def _build_prompt(self, req: SymptomAssessmentRequest) -> str:
        lang = "Tamil" if req.language == LanguageChoice.TA else "English"
        return f"""
You are the educational assistant for HealthGuide AI.
The user provided:
- Age bracket: {req.age_range.value}
- Symptoms: "{req.symptoms_text}"
- Duration: {req.duration.value}
- Self-reported severity: {req.severity.value}
- Additional context: "{req.additional_context or 'None'}"
- Response language: {lang}

SAFETY DIRECTIVES:
1. You are NOT a doctor and CANNOT diagnose any medical condition.
2. NEVER prescribe medications, specific dosages, or suggest stopping medical treatments.
3. NEVER fabricate clinical probabilities, fake disease percentages (e.g. "85% chance of X"), or invent statistical citations.
4. Output MUST be valid JSON matching this schema:
{{
  "urgency_level": "SEEK_CARE_SOON" or "SELF_CARE_MONITOR" or "AMBIGUOUS_CONSULT_CLINICIAN",
  "observed_signals": [{{"label": "string", "description": "string"}}],
  "possible_explanations": [{{"title": "string", "description": "string", "educational_context": "string"}}],
  "self_care_guidance": [{{"category": "string", "tip": "string"}}],
  "next_steps": ["string", "string"],
  "uncertainty_notice": "string",
  "disclaimer": "string"
}}
"""

    def _parse_and_validate_ai_json(
        self, raw_text: str, fallback: AssessmentResponse, language: LanguageChoice
    ) -> Optional[AssessmentResponse]:
        try:
            parsed = json.loads(raw_text)
            # Enforce that LLM cannot output EMERGENCY or override deterministic emergency handling
            urgency_str = parsed.get("urgency_level", fallback.urgency_level.value)
            if urgency_str not in [
                UrgencyLevel.SEEK_CARE_SOON.value,
                UrgencyLevel.SELF_CARE_MONITOR.value,
                UrgencyLevel.AMBIGUOUS_CONSULT_CLINICIAN.value,
            ]:
                urgency = fallback.urgency_level
            else:
                urgency = UrgencyLevel(urgency_str)

            # Build validated response merging AI educational text with curated sources and safety notices
            return AssessmentResponse(
                urgency_level=urgency,
                is_emergency=False,
                emergency_notice=None,
                observed_signals=parsed.get("observed_signals", fallback.observed_signals),
                possible_explanations=parsed.get("possible_explanations", fallback.possible_explanations),
                self_care_guidance=parsed.get("self_care_guidance", fallback.self_care_guidance),
                next_steps=parsed.get("next_steps", fallback.next_steps),
                uncertainty_notice=parsed.get("uncertainty_notice", fallback.uncertainty_notice),
                disclaimer=fallback.disclaimer,  # Always use vetted static disclaimer
                trusted_sources=fallback.trusted_sources,  # Always use verified curated sources
                language=language.value,
                engine_source="hybrid_with_verified_ai",
            )
        except Exception:
            return None
