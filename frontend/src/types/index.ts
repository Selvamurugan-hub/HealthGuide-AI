export type AgeRange =
  | 'CHILD_0_12'
  | 'TEEN_13_17'
  | 'ADULT_18_64'
  | 'OLDER_ADULT_65_PLUS';

export type SeverityLevel = 'MILD' | 'MODERATE' | 'SEVERE' | 'CRITICAL';

export type DurationCategory =
  | 'LESS_THAN_24_HOURS'
  | 'DAYS_1_TO_3'
  | 'DAYS_4_TO_7'
  | 'WEEKS_1_TO_2'
  | 'MORE_THAN_2_WEEKS';

export type LanguageChoice = 'en' | 'ta';

export type UrgencyLevel =
  | 'EMERGENCY'
  | 'SEEK_CARE_SOON'
  | 'SELF_CARE_MONITOR'
  | 'AMBIGUOUS_CONSULT_CLINICIAN';

export interface SymptomAssessmentRequest {
  age_range: AgeRange;
  symptoms_text: string;
  duration: DurationCategory;
  severity: SeverityLevel;
  additional_context?: string;
  language: LanguageChoice;
}

export interface EmergencyNotice {
  title: string;
  message: string;
  action_call: string;
  emergency_numbers: string[];
  warning_signs_detected: string[];
}

export interface ObservedSignal {
  label: string;
  description: string;
}

export interface PossibleExplanation {
  title: string;
  description: string;
  educational_context: string;
}

export interface SelfCareAdvice {
  category: string;
  tip: string;
}

export interface TrustedSource {
  name: string;
  url: string;
  description: string;
  relevance_note: string;
}

export interface AssessmentResponse {
  urgency_level: UrgencyLevel;
  is_emergency: boolean;
  emergency_notice?: EmergencyNotice | null;
  observed_signals: ObservedSignal[];
  possible_explanations: PossibleExplanation[];
  self_care_guidance: SelfCareAdvice[];
  next_steps: string[];
  uncertainty_notice: string;
  disclaimer: string;
  trusted_sources: TrustedSource[];
  language: string;
  engine_source: string;
}
