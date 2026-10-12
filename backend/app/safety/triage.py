from typing import List, Optional
from ..models import (
    AgeRange,
    AssessmentResponse,
    EmergencyNotice,
    LanguageChoice,
    ObservedSignal,
    PossibleExplanation,
    SelfCareAdvice,
    SeverityLevel,
    SymptomAssessmentRequest,
    TrustedSource,
    UrgencyLevel,
)
from .detector import EmergencyDetector, WarningSignMatch
from ..services.curated_knowledge import (
    CURATED_TRUSTED_SOURCES,
    match_curated_pattern,
)


class SafetyTriageEngine:
    def __init__(self, detector: Optional[EmergencyDetector] = None):
        self.detector = detector or EmergencyDetector()

    def assess(self, request: SymptomAssessmentRequest) -> AssessmentResponse:
        is_tamil = request.language == LanguageChoice.TA
        
        # 1. First priority: Deterministic Emergency Scan
        emergency_matches = self.detector.scan(
            text=request.symptoms_text,
            context=request.additional_context,
        )

        if emergency_matches:
            return self._build_emergency_response(request, emergency_matches, is_tamil)

        # 2. Check for severe unclassified symptoms
        if request.severity == SeverityLevel.CRITICAL or request.severity == SeverityLevel.SEVERE:
            return self._build_high_severity_response(request, is_tamil)

        # 3. Check for curated educational patterns
        curated_match = match_curated_pattern(
            text=request.symptoms_text,
            context=request.additional_context,
        )

        if curated_match:
            return self._build_curated_response(request, curated_match, is_tamil)

        # 4. Ambiguous / Unclassified safe fallback
        return self._build_ambiguous_response(request, is_tamil)

    def _build_emergency_response(
        self,
        request: SymptomAssessmentRequest,
        matches: List[WarningSignMatch],
        is_tamil: bool,
    ) -> AssessmentResponse:
        detected_names = [
            m.rule_name_ta if is_tamil else m.rule_name_en for m in matches
        ]

        if is_tamil:
            title = "உடனடி அவசர மருத்துவ உதவி தேவை (அவசர எச்சரிக்கை)"
            message = (
                "உங்கள் விளக்கத்தில் அவசர மருத்துவ கவனிப்பு தேவைப்படக்கூடிய தீவிர எச்சரிக்கை அறிகுறிகள் கண்டறியப்பட்டுள்ளன. "
                "தாமதிக்காமல் உடனடியாக அவசர மருத்துவ சேவையை அழைக்கவும்."
            )
            action_call = "உடனடியாக அவசர ஊர்தி (108 / 112 / 911) அழைக்கவும் அல்லது அருகில் உள்ள அவசர சிகிச்சைப் பிரிவிற்குச் செல்லவும்."
            disclaimer = (
                "இது ஒரு தகவல் மற்றும் விழிப்புணர்வு மாதிரி மட்டுமே; மருத்துவ நோயறிதல் அல்ல. "
                "உடனடி மருத்துவ சிகிச்சைக்கு மாற்றாக இதைப் பயன்படுத்தக் கூடாது."
            )
            uncertainty_notice = (
                "அவசரநிலை கண்டறியும் விதிகளின் அடிப்படையில் இந்த எச்சரிக்கை முன்னுரிமை அளிக்கப்பட்டு உடனடியாக காட்டப்படுகிறது. "
                "தானியங்கி சோதனைகள் மருத்துவ பரிசோதனையை ஈடுசெய்ய முடியாது."
            )
            next_steps = [
                "உடனடியாக அவசர சிகிச்சை உதவி எண்களை (108 / 112 / 911) அழைக்கவும்.",
                "நீங்களாக வாகனத்தை ஓட்ட வேண்டாம்; நண்பர், குடும்பத்தினர் அல்லது ஆம்புலன்ஸ் உதவியை நாடவும்.",
                "அமைதியாக அமர்ந்து, ஆசுவாசப்படுத்திக் கொள்ளவும்; உடனிருக்கும் நபருக்கு உங்கள் நிலையைத் தெரிவிக்கவும்.",
                "மருத்துவ ஆலோசனை இன்றி சுயமாக எவ்வித மருந்துகளையும் உட்கொள்ள வேண்டாம்.",
            ]
            signals = [
                ObservedSignal(
                    label=m.rule_name_ta,
                    description=f"கண்டறியப்பட்ட அவசர அறிகுறி: '{m.matched_snippet}'. {m.description_ta}",
                )
                for m in matches
            ]
            explanations = [
                PossibleExplanation(
                    title="சாத்தியமான தீவிர அவசர மருத்துவ நிலை",
                    description="இந்த அறிகுறிகள் தீவிர இருதய, சுவாச அல்லது நரம்பியல் குறைபாடுகளோடு தொடர்புடையதாக இருக்கலாம்.",
                    educational_context="அவசர அறிகுறிகள் தோன்றும் போது உடனடி மருத்துவ பரிசோதனையே உயிர்காக்கும் மிக முக்கியமான படியாகும்.",
                )
            ]
        else:
            title = "Immediate Emergency Evaluation Recommended (Warning Flag)"
            message = (
                "Your description contains potential red-flag warning signs that require urgent clinical attention. "
                "Do not wait. Please contact emergency medical services or go to the nearest emergency department right away."
            )
            action_call = "Call emergency services (911 / 112 / 999 / 108) or proceed to the nearest emergency room immediately."
            disclaimer = (
                "This educational prototype is NOT a diagnostic tool and does NOT replace a licensed healthcare professional. "
                "Emergency symptoms require immediate physical clinical care."
            )
            uncertainty_notice = (
                "Automated symptom screening has strict limitations and cannot rule out serious or life-threatening conditions. "
                "Because red-flag markers were detected, this warning takes absolute priority."
            )
            next_steps = [
                "Call your local emergency number (e.g. 911, 112, 108, or 999) immediately.",
                "Do not attempt to drive yourself to the emergency department. Seek help from an ambulance or a companion.",
                "Notify someone nearby about what you are experiencing so you are not alone.",
                "Do not take unprescribed medications or delay emergency evaluation for home remedies.",
            ]
            signals = [
                ObservedSignal(
                    label=m.rule_name_en,
                    description=f"Critical signal detected: '{m.matched_snippet}'. {m.description_en}",
                )
                for m in matches
            ]
            explanations = [
                PossibleExplanation(
                    title="Potential Acute Medical Emergency",
                    description="The reported signs may reflect an acute cardiovascular, neurological, respiratory, or systemic crisis.",
                    educational_context="Prompt clinical intervention significantly improves patient outcomes during acute events.",
                )
            ]

        # Select relevant sources for emergency
        sources = [
            CURATED_TRUSTED_SOURCES["medlineplus_chest"],
            CURATED_TRUSTED_SOURCES["nhs_chest"],
            CURATED_TRUSTED_SOURCES["medlineplus_general"],
        ]

        return AssessmentResponse(
            urgency_level=UrgencyLevel.EMERGENCY,
            is_emergency=True,
            emergency_notice=EmergencyNotice(
                title=title,
                message=message,
                action_call=action_call,
                emergency_numbers=["112 (Universal / India / EU)", "108 (India Ambulance)", "911 (US / Canada)", "999 (UK)"],
                warning_signs_detected=detected_names,
            ),
            observed_signals=signals,
            possible_explanations=explanations,
            self_care_guidance=[],  # Deliberately empty: do not give home self-care during active emergencies
            next_steps=next_steps,
            uncertainty_notice=uncertainty_notice,
            disclaimer=disclaimer,
            trusted_sources=sources,
            language="ta" if is_tamil else "en",
            engine_source="deterministic_safety_engine",
        )

    def _build_high_severity_response(
        self,
        request: SymptomAssessmentRequest,
        is_tamil: bool,
    ) -> AssessmentResponse:
        if is_tamil:
            uncertainty_notice = (
                "நீங்கள் தீவிரமான அசௌகரியத்தைத் தேர்ந்தெடுத்துள்ளீர்கள். நேரடி மருத்துவ பரிசோதனை இன்றி இதன் காரணத்தை உறுதி செய்ய இயலாது."
            )
            disclaimer = "இது ஒரு மருத்துவ ஆலோசனையோ நோயறிதலோ அல்ல. எப்போதும் மருத்துவரை அணுகவும்."
            next_steps = [
                "அடுத்த சில மணிநேரங்களுக்குள் அல்லது இன்றே மருத்துவரை அல்லது அவசர மருத்துவ மையத்தை அணுகவும்.",
                "சுவாசத் திணறல், தீவிர மார்பு வலி அல்லது சுயநினைவு இழப்பு ஏற்பட்டால் உடனடியாக அவசர சிகிச்சைப் பிரிவுக்குச் செல்லவும்.",
                "உங்கள் அறிகுறிகள் எப்போது தொடங்கின, என்னென்ன மாற்றங்கள் ஏற்பட்டுள்ளன என்பதை குறித்து வைத்து மருத்துவரிடம் பகிரவும்.",
            ]
            signals = [
                ObservedSignal(
                    label="உயர் தீவிர அறிகுறி எச்சரிக்கை",
                    description=f"தீவிர நிலை: {request.severity.value}. தீவிர அசௌகரியம் விரைவான மருத்துவ ஆலோசனையைக் கோருகிறது.",
                )
            ]
            explanations = [
                PossibleExplanation(
                    title="விரிவான மருத்துவ பரிசோதனை தேவைப்படும் தீவிர நிலை",
                    description="தீவிர அறிகுறிகள் எளிய காரணங்களாலும் வரலாம், அல்லது உடற்கூறு பரிசோதனை தேவைப்படும் கோளாறுகளாகவும் இருக்கலாம்.",
                    educational_context="தொடர்ச்சியான கடுமையான வலி அல்லது தீவிர உடல் உபாதைகளை தாமதமின்றி மருத்துவரிடம் காட்ட வேண்டும்.",
                )
            ]
        else:
            uncertainty_notice = (
                "You indicated a high severity level. Automated tools cannot substitute for a physical clinical examination or laboratory evaluation."
            )
            disclaimer = "HealthGuide AI provides educational information only and cannot diagnose illness or prescribe treatments."
            next_steps = [
                "Contact a primary care physician, urgent care clinic, or telehealth provider today.",
                "Seek emergency care immediately if you develop difficulty breathing, severe chest pain, sudden weakness, or confusion.",
                "Keep a written log of when symptoms began, what makes them better or worse, and any medications taken.",
            ]
            signals = [
                ObservedSignal(
                    label="High Severity Discomfort Indicated",
                    description=f"Recorded severity: {request.severity.value}. Marked discomfort warrants timely professional medical assessment.",
                )
            ]
            explanations = [
                PossibleExplanation(
                    title="Acute Discomfort Requiring Clinical Review",
                    description="High-severity symptoms can stem from various causes that cannot be distinguished safely without medical history and diagnostics.",
                    educational_context="A clinician can check vital signs and order targeted tests to provide personalized medical care.",
                )
            ]

        return AssessmentResponse(
            urgency_level=UrgencyLevel.SEEK_CARE_SOON,
            is_emergency=False,
            emergency_notice=None,
            observed_signals=signals,
            possible_explanations=explanations,
            self_care_guidance=[],
            next_steps=next_steps,
            uncertainty_notice=uncertainty_notice,
            disclaimer=disclaimer,
            trusted_sources=[
                CURATED_TRUSTED_SOURCES["medlineplus_general"],
                CURATED_TRUSTED_SOURCES["nhs_general"],
            ],
            language="ta" if is_tamil else "en",
            engine_source="deterministic_safety_engine",
        )

    def _build_curated_response(
        self,
        request: SymptomAssessmentRequest,
        pattern,
        is_tamil: bool,
    ) -> AssessmentResponse:
        signals = pattern.signals_ta if is_tamil else pattern.signals_en
        explanations = pattern.explanations_ta if is_tamil else pattern.explanations_en
        self_care = pattern.self_care_ta if is_tamil else pattern.self_care_en
        next_steps = pattern.next_steps_ta if is_tamil else pattern.next_steps_en

        if is_tamil:
            uncertainty = (
                "இங்கு குறிப்பிடப்பட்டுள்ள காரணங்கள் கல்வி நோக்கத்திற்கான பொதுவான தகவல்களே; உங்கள் தனிப்பட்ட மருத்துவ நோயறிதல் அல்ல. "
                "உடல்நிலை மாற்றங்களை தொடர்ந்து கவனிக்கவும்."
            )
            disclaimer = "இது ஒரு கல்வி மாதிரி மட்டுமே. மருத்துவ பரிசோதனைக்கு மாற்றாகாது."
        else:
            uncertainty = (
                "These potential explanations are general educational possibilities based on curated clinical knowledge. "
                "They are not a diagnosis and cannot rule out other underlying health conditions."
            )
            disclaimer = "HealthGuide AI is an educational prototype and not a diagnosis. Never ignore professional medical advice or delay seeking care."

        return AssessmentResponse(
            urgency_level=pattern.urgency,
            is_emergency=False,
            emergency_notice=None,
            observed_signals=signals,
            possible_explanations=explanations,
            self_care_guidance=self_care,
            next_steps=next_steps,
            uncertainty_notice=uncertainty,
            disclaimer=disclaimer,
            trusted_sources=pattern.sources,
            language="ta" if is_tamil else "en",
            engine_source="deterministic_safety_engine",
        )

    def _build_ambiguous_response(
        self,
        request: SymptomAssessmentRequest,
        is_tamil: bool,
    ) -> AssessmentResponse:
        if is_tamil:
            signals = [
                ObservedSignal(
                    label="பொதுவான அல்லது குறிப்பிட்ட வகைப்படுத்தப்படாத அறிகுறிகள்",
                    description="வழங்கப்பட்ட தகவல் உடனடி அவசர எச்சரிக்கை விதிகளைத் தூண்டவில்லை, ஆனால் எளிய பொதுவான வகைகளுடனும் பொருந்தவில்லை.",
                )
            ]
            explanations = [
                PossibleExplanation(
                    title="வரையறுக்கப்படாத உடல் அசௌகரியம்",
                    description="அறிகுறிகள் பலவித காரணங்களால் தோன்றக்கூடும். நேரடி மருத்துவ கலந்துரையாடல் மூலம் மட்டுமே இதை சரியாக மதிப்பீடு செய்ய முடியும்.",
                    educational_context="மனித உடலின் பல அறிகுறிகள் ஒன்றுடன் ஒன்று தொடர்புடையதாக இருப்பதால் மருத்துவ பரிசோதனை அவசியமானது.",
                )
            ]
            next_steps = [
                "அறிகுறிகள் நீடித்தாலோ அல்லது தொந்தரவு செய்தாலோ உங்கள் மருத்துவரை அணுகவும்.",
                "மார்பு வலி, மூச்சுத் திணறல், கடுமையான தலைவலி போன்ற எச்சரிக்கை அறிகுறிகள் தென்பட்டால் உடனே அவசர சிகிச்சை பெறவும்.",
                "அறிகுறிகளின் கால அளவு மற்றும் தன்மையைக் குறித்து வைத்து மருத்துவரிடம் விளக்கலாம்.",
            ]
            self_care = [
                SelfCareAdvice(
                    category="பொதுவான கவனிப்பு",
                    tip="போதுமான ஓய்வு எடுக்கவும், போதுமான நீர் அருந்தவும், உடல் சோர்வை தவிர்க்கவும்.",
                )
            ]
            uncertainty = (
                "அமைப்பால் இந்த அறிகுறிகளை நம்பிக்கையுடன் வகைப்படுத்த முடியவில்லை. உண்மைக்குப் புறம்பான தகவல்களைத் தருவதைத் தவிர்த்து, மருத்துவ ஆலோசனையை பரிந்துரைக்கிறோம்."
            )
            disclaimer = "இது ஒரு மருத்துவ நோயறிதல் அல்ல. சந்தேகம் இருப்பின் மருத்துவரை ஆலோசிக்கவும்."
        else:
            signals = [
                ObservedSignal(
                    label="Unclassified or Ambiguous Symptom Presentation",
                    description="No immediate red-flag emergency keywords were detected, but the description does not safely match a narrow routine profile.",
                )
            ]
            explanations = [
                PossibleExplanation(
                    title="Non-Specific Discomfort",
                    description="Symptoms can arise from diverse clinical etiologies that require physical history taking, vital sign checks, and personalized assessment.",
                    educational_context="Rather than generating an unverified statistical guess, we recommend discussing your health with a licensed practitioner.",
                )
            ]
            next_steps = [
                "Schedule a routine consultation with a healthcare provider if symptoms persist or interfere with your daily routine.",
                "Seek immediate emergency care if new warning signs emerge (such as chest pain, breathing difficulty, or fainting).",
                "Keep note of symptom frequency and any specific environmental or food triggers.",
            ]
            self_care = [
                SelfCareAdvice(
                    category="General Well-being",
                    tip="Maintain adequate hydration, prioritize healthy rest, and avoid strenuous physical overexertion.",
                )
            ]
            uncertainty = (
                "The automated engine cannot confidently categorize this description. Rather than speculating, we advise consulting a doctor."
            )
            disclaimer = "HealthGuide AI is an educational tool, not a doctor. It cannot provide a definitive diagnosis."

        return AssessmentResponse(
            urgency_level=UrgencyLevel.AMBIGUOUS_CONSULT_CLINICIAN,
            is_emergency=False,
            emergency_notice=None,
            observed_signals=signals,
            possible_explanations=explanations,
            self_care_guidance=self_care,
            next_steps=next_steps,
            uncertainty_notice=uncertainty,
            disclaimer=disclaimer,
            trusted_sources=[
                CURATED_TRUSTED_SOURCES["medlineplus_general"],
                CURATED_TRUSTED_SOURCES["nhs_general"],
            ],
            language="ta" if is_tamil else "en",
            engine_source="deterministic_safety_engine",
        )
