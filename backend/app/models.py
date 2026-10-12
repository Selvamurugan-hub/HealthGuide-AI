from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class AgeRange(str, Enum):
    CHILD_0_12 = "CHILD_0_12"
    TEEN_13_17 = "TEEN_13_17"
    ADULT_18_64 = "ADULT_18_64"
    OLDER_ADULT_65_PLUS = "OLDER_ADULT_65_PLUS"


class SeverityLevel(str, Enum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"
    CRITICAL = "CRITICAL"


class DurationCategory(str, Enum):
    LESS_THAN_24_HOURS = "LESS_THAN_24_HOURS"
    DAYS_1_TO_3 = "DAYS_1_TO_3"
    DAYS_4_TO_7 = "DAYS_4_TO_7"
    WEEKS_1_TO_2 = "WEEKS_1_TO_2"
    MORE_THAN_2_WEEKS = "MORE_THAN_2_WEEKS"


class LanguageChoice(str, Enum):
    EN = "en"
    TA = "ta"


class UrgencyLevel(str, Enum):
    EMERGENCY = "EMERGENCY"
    SEEK_CARE_SOON = "SEEK_CARE_SOON"
    SELF_CARE_MONITOR = "SELF_CARE_MONITOR"
    AMBIGUOUS_CONSULT_CLINICIAN = "AMBIGUOUS_CONSULT_CLINICIAN"


class SymptomAssessmentRequest(BaseModel):
    age_range: AgeRange
    symptoms_text: str = Field(
        ...,
        min_length=3,
        max_length=1500,
        description="Main symptoms described in user's own words",
    )
    duration: DurationCategory
    severity: SeverityLevel
    additional_context: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional context like pre-existing conditions or triggers",
    )
    language: LanguageChoice = Field(
        default=LanguageChoice.EN,
        description="Preferred response language (en or ta)",
    )

    @field_validator("symptoms_text")
    @classmethod
    def validate_non_whitespace(cls, v: str) -> str:
        cleaned = v.strip()
        if len(cleaned) < 3:
            raise ValueError("Symptoms description must contain at least 3 non-whitespace characters.")
        return cleaned


class EmergencyNotice(BaseModel):
    title: str
    message: str
    action_call: str
    emergency_numbers: List[str]
    warning_signs_detected: List[str]


class ObservedSignal(BaseModel):
    label: str
    description: str


class PossibleExplanation(BaseModel):
    title: str
    description: str
    educational_context: str


class SelfCareAdvice(BaseModel):
    category: str
    tip: str


class TrustedSource(BaseModel):
    name: str
    url: str
    description: str
    relevance_note: str


class AssessmentResponse(BaseModel):
    urgency_level: UrgencyLevel
    is_emergency: bool
    emergency_notice: Optional[EmergencyNotice] = None
    observed_signals: List[ObservedSignal] = []
    possible_explanations: List[PossibleExplanation] = []
    self_care_guidance: List[SelfCareAdvice] = []
    next_steps: List[str] = []
    uncertainty_notice: str
    disclaimer: str
    trusted_sources: List[TrustedSource] = []
    language: str = "en"
    engine_source: str = "deterministic_safety_engine"
