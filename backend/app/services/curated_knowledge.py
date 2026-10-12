import re
from typing import Dict, List, Optional
from ..models import (
    ObservedSignal,
    PossibleExplanation,
    SelfCareAdvice,
    TrustedSource,
    UrgencyLevel,
)

CURATED_TRUSTED_SOURCES = {
    "medlineplus_general": TrustedSource(
        name="MedlinePlus (National Library of Medicine)",
        url="https://medlineplus.gov/",
        description="High-quality, reliable, and clinically vetted health information from the US National Institutes of Health.",
        relevance_note="General patient education and symptom library.",
    ),
    "nhs_general": TrustedSource(
        name="NHS UK Health A to Z",
        url="https://www.nhs.uk/",
        description="Official National Health Service guide to conditions, symptoms, and when to seek medical treatment.",
        relevance_note="Evidence-based clinical guidance and triage timelines.",
    ),
    "medlineplus_chest": TrustedSource(
        name="MedlinePlus: Chest Pain Guide",
        url="https://medlineplus.gov/chestpain.html",
        description="Comprehensive emergency guidance on chest discomfort, cardiovascular evaluation, and red flags.",
        relevance_note="Specific guidance for sudden chest tightness or cardiac warning signs.",
    ),
    "nhs_chest": TrustedSource(
        name="NHS: Chest Pain Assessment",
        url="https://www.nhs.uk/conditions/chest-pain/",
        description="Clinical triage instructions for chest pain and when to call emergency services immediately.",
        relevance_note="Guidance on identifying cardiac and respiratory emergencies.",
    ),
    "medlineplus_headache": TrustedSource(
        name="MedlinePlus: Headache Overview",
        url="https://medlineplus.gov/headache.html",
        description="Information on tension headaches, migraines, sinus headaches, and neurological warning signs.",
        relevance_note="Patient education regarding persistent or recurrent head pain.",
    ),
    "nhs_headache": TrustedSource(
        name="NHS: Headaches and Migraines",
        url="https://www.nhs.uk/conditions/headaches/",
        description="NHS guidelines on common causes of headaches and red-flag symptoms.",
        relevance_note="Information on self-care and medical consultation criteria.",
    ),
    "medlineplus_cold": TrustedSource(
        name="MedlinePlus: Common Cold and Flu",
        url="https://medlineplus.gov/commoncold.html",
        description="Evidence-based overview of viral respiratory tract infections, fever management, and recovery.",
        relevance_note="Education on viral symptom progression and hydration.",
    ),
    "nhs_cold": TrustedSource(
        name="NHS: Common Cold Symptoms & Management",
        url="https://www.nhs.uk/conditions/common-cold/",
        description="Official NHS advice on resting, fluids, and signs of secondary respiratory complications.",
        relevance_note="Support for managing viral symptoms safely at home.",
    ),
}


class CuratedConditionPattern:
    def __init__(
        self,
        key: str,
        keywords: List[str],
        urgency: UrgencyLevel,
        signals_en: List[ObservedSignal],
        signals_ta: List[ObservedSignal],
        explanations_en: List[PossibleExplanation],
        explanations_ta: List[PossibleExplanation],
        self_care_en: List[SelfCareAdvice],
        self_care_ta: List[SelfCareAdvice],
        next_steps_en: List[str],
        next_steps_ta: List[str],
        sources: List[TrustedSource],
    ):
        self.key = key
        ascii_kw = [re.escape(k) for k in keywords if k.isascii()]
        unicode_kw = [k for k in keywords if not k.isascii()]
        self.ascii_regex = re.compile(r"\b(" + "|".join(ascii_kw) + r")\b", re.IGNORECASE) if ascii_kw else None
        self.unicode_keywords = [k.lower() for k in unicode_kw]
        self.urgency = urgency
        self.signals_en = signals_en
        self.signals_ta = signals_ta
        self.explanations_en = explanations_en
        self.explanations_ta = explanations_ta
        self.self_care_en = self_care_en
        self.self_care_ta = self_care_ta
        self.next_steps_en = next_steps_en
        self.next_steps_ta = next_steps_ta
        self.sources = sources

    def matches(self, text: str) -> bool:
        lower_text = text.lower()
        if self.ascii_regex and self.ascii_regex.search(lower_text):
            return True
        for uk in self.unicode_keywords:
            if uk in lower_text:
                return True
        return False


CURATED_PATTERNS: List[CuratedConditionPattern] = [
    # 1. Headache / Tension / Migraine
    CuratedConditionPattern(
        key="headache",
        keywords=[
            "headache",
            "head ache",
            "migraine",
            "throbbing head",
            "temple pain",
            "forehead ache",
            "தலைவலி",
            "ஒற்றைத் தலைவலி",
            "thalaivali",
        ],
        urgency=UrgencyLevel.SELF_CARE_MONITOR,
        signals_en=[
            ObservedSignal(
                label="Headache Discomfort",
                description="Reported pain in the head or temples without detected acute neurological warning signs.",
            )
        ],
        signals_ta=[
            ObservedSignal(
                label="தலைவலி அசௌகரியம்",
                description="நரம்பியல் அவசர அறிகுறிகள் ஏதுமின்றி தலை அல்லது நெற்றிப் பகுதியில் பதிவான வலி.",
            )
        ],
        explanations_en=[
            PossibleExplanation(
                title="Tension-Type Headache or Musculoskeletal Stress",
                description="Often associated with physical fatigue, prolonged screen exposure, neck muscle tightness, or stress.",
                educational_context="Tension headaches are the most frequent type of headache and typically feel like a dull band across the forehead or back of the head.",
            ),
            PossibleExplanation(
                title="Migraine without Aura or Dehydration Headache",
                description="May present with moderate throbbing, sensitivity to bright light or sound, or fluid deficit.",
                educational_context="Migraines often occur episodically and can be triggered by lack of sleep, hormonal changes, or specific dietary elements.",
            ),
        ],
        explanations_ta=[
            PossibleExplanation(
                title="அழுத்தம் அல்லது சோர்வு சார்ந்த தலைவலி (Tension Headache)",
                description="மன அழுத்தம், நீண்ட நேரம் கணினித் திரை பார்த்தல், கழுத்துத் தசை இறுக்கம் அல்லது தூக்கமின்மை ஆகியவற்றால் வரக்கூடியது.",
                educational_context="இது மிகவும் பொதுவான தலைவலி வகையாகும்; தலை முழுவதும் ஒரு இறுக்கமான உணர்வு ஏற்படலாம்.",
            ),
            PossibleExplanation(
                title="ஒற்றைத் தலைவலி அல்லது நீரிழப்பு (Migraine / Dehydration)",
                description="ஒளி மற்றும் சத்தத்தின் மீது கூச்ச உணர்வு, நீர் சத்துக் குறைவு அல்லது துடிக்கும் வலி வரக்கூடும்.",
                educational_context="போதிய நீர் அருந்தாமை மற்றும் சீரற்ற உணவுப் பழக்கம் இதனைத் தூண்டலாம்.",
            ),
        ],
        self_care_en=[
            SelfCareAdvice(
                category="Rest & Environment",
                tip="Rest in a quiet, dimly lit room. Avoid prolonged smartphone or monitor screens.",
            ),
            SelfCareAdvice(
                category="Hydration",
                tip="Drink adequate water throughout the day. Mild dehydration is a frequent headache contributor.",
            ),
            SelfCareAdvice(
                category="Comfort Measures",
                tip="Apply a cool or warm compress gently across the forehead or back of the neck.",
            ),
        ],
        self_care_ta=[
            SelfCareAdvice(
                category="ஓய்வு மற்றும் சூழல்",
                tip="அமைதியான, மிதமான வெளிச்சம் கொண்ட அறையில் ஓய்வெடுக்கவும். திரை நேரத்தைக் குறைக்கவும்.",
            ),
            SelfCareAdvice(
                category="நீர்ச்சத்து",
                tip="நாள் முழுவதும் போதுமான அளவு தண்ணீர் குடிக்கவும்; உடலில் நீர் குறைவது தலைவலியை உண்டாக்கலாம்.",
            ),
            SelfCareAdvice(
                category="ஆறுதல் நடவடிக்கைகள்",
                tip="நெற்றி அல்லது கழுத்துப் பகுதியில் மென்மையான குளிர்ந்த அல்லது வெதுவெதுப்பான ஒத்தடம் கொடுக்கலாம்.",
            ),
        ],
        next_steps_en=[
            "Monitor symptoms for next 24-48 hours.",
            "Schedule an appointment with a primary care clinician if headaches recur frequently, worsen progressively, or interfere with daily activities.",
            "Seek emergency care immediately if you develop sudden 'worst headache of life', stiff neck with fever, confusion, or visual loss.",
        ],
        next_steps_ta=[
            "அடுத்த 24-48 மணிநேரத்திற்கு அறிகுறிகளைக் கவனிக்கவும்.",
            "தலைவலி அடிக்கடி ஏற்பட்டாலோ அல்லது தீவிரமடைந்தாலோ மருத்துவரை அணுகவும்.",
            "திடீர் தாங்க முடியாத தீவிர தலைவலி, கழுத்து விரைப்பு, காய்ச்சல் அல்லது பார்வை மங்குதல் ஏற்பட்டால் உடனே அவசர சிகிச்சைப் பிரிவை நாடவும்.",
        ],
        sources=[
            CURATED_TRUSTED_SOURCES["medlineplus_headache"],
            CURATED_TRUSTED_SOURCES["nhs_headache"],
        ],
    ),
    # 2. Common Cold / Upper Respiratory / Cough / Sore Throat
    CuratedConditionPattern(
        key="respiratory_viral",
        keywords=[
            "cold",
            "cough",
            "runny nose",
            "stuffy nose",
            "sore throat",
            "sneezing",
            "mild fever",
            "congestion",
            "இருமல்",
            "சளி",
            "தொண்டை வலி",
            "மூக்கடைப்பு",
            "irumal",
            "sali",
        ],
        urgency=UrgencyLevel.SELF_CARE_MONITOR,
        signals_en=[
            ObservedSignal(
                label="Upper Respiratory Tract Irritation",
                description="Common nasal, throat, or mild bronchial symptoms consistent with viral or seasonal changes.",
            )
        ],
        signals_ta=[
            ObservedSignal(
                label="மேல் சுவாசப்பாதை எரிச்சல்",
                description="வைரஸ் அல்லது பருவகால மாற்றங்களால் ஏற்படும் மூக்கு, தொண்டை எரிச்சல் அறிகுறிகள்.",
            )
        ],
        explanations_en=[
            PossibleExplanation(
                title="Common Viral Upper Respiratory Infection",
                description="Typically caused by rhinoviruses or other common respiratory viruses.",
                educational_context="Most uncomplicated viral colds run their course within 7 to 10 days with gradual improvement.",
            ),
            PossibleExplanation(
                title="Seasonal Allergic Rhinitis",
                description="Inflammation of the nasal mucous membranes from pollen, dust mites, or environmental allergens.",
                educational_context="Allergies often feature clear nasal discharge, repetitive sneezing, and itchy eyes or palate.",
            ),
        ],
        explanations_ta=[
            PossibleExplanation(
                title="பொதுவான மேல் சுவாசப்பாதை வைரஸ் தொற்று (சளி / இருமல்)",
                description="ரைனோவைரஸ் போன்ற பொதுவான வைரஸ்களால் வரக்கூடிய எளிய சளித் தொற்று.",
                educational_context="பெரும்பாலான எளிய சளித் தொற்றுகள் 7 முதல் 10 நாட்களுக்குள் படிப்படியாக குணமாகும்.",
            ),
            PossibleExplanation(
                title="பருவகால ஒவ்வாமை (Seasonal Allergic Rhinitis)",
                description="தூசி, பூந்துகள் அல்லது சுற்றுச்சூழல் காரணிகளால் ஏற்படும் மூக்கு மற்றும் தொண்டை எரிச்சல்.",
                educational_context="தொடர் தும்மல், தெளிவான மூக்கு நீர் வடிதல் மற்றும் அரிப்பு ஆகியவை இதில் பொதுவாக காணப்படும்.",
            ),
        ],
        self_care_en=[
            SelfCareAdvice(
                category="Hydration",
                tip="Sip warm liquids such as herbal tea, warm water with lemon, or clear broth to soothe throat membranes.",
            ),
            SelfCareAdvice(
                category="Rest",
                tip="Prioritize sleep and physical rest to support your immune system's natural recovery.",
            ),
            SelfCareAdvice(
                category="Humidification",
                tip="Use steam inhalation or a cool-mist humidifier to ease nasal congestion and airway dryness.",
            ),
        ],
        self_care_ta=[
            SelfCareAdvice(
                category="வெதுவெதுப்பான நீர் அருந்துதல்",
                tip="தொண்டை எரிச்சலைத் தணிக்க வெதுவெதுப்பான நீர், மூலிகை தேநீர் அல்லது சூப் பருகவும்.",
            ),
            SelfCareAdvice(
                category="ஓய்வு",
                tip="உடலின் நோய் எதிர்ப்பு ஆற்றல் மீள போதுமான அளவு தூங்கி ஓய்வெடுக்கவும்.",
            ),
            SelfCareAdvice(
                category="நீராவி பிடித்தல்",
                tip="மூக்கடைப்பைத் தளர்த்த மிதமான நீராவி பிடிக்கலாம்.",
            ),
        ],
        next_steps_en=[
            "Monitor body temperature and symptom progression for 3-5 days.",
            "Contact a doctor if fever stays above 38.5°C (101.3°F) for more than 3 days, or if symptoms worsen after a week.",
            "Seek emergency evaluation if you develop shortness of breath, chest pain, or difficulty swallowing fluids.",
        ],
        next_steps_ta=[
            "அடுத்த 3-5 நாட்களுக்கு உடல் வெப்பநிலையையும் அறிகுறிகளையும் கவனிக்கவும்.",
            "3 நாட்களுக்கு மேல் அதிக காய்ச்சல் நீடித்தாலோ அல்லது நிலைமை மோசமானாலோ மருத்துவரை அணுகவும்.",
            "மூச்சுத் திணறல், மார்பு வலி அல்லது உமிழ்நீரைக் கூட விழுங்க முடியாத நிலை ஏற்பட்டால் உடனே அவசர சிகிச்சை பெறவும்.",
        ],
        sources=[
            CURATED_TRUSTED_SOURCES["medlineplus_cold"],
            CURATED_TRUSTED_SOURCES["nhs_cold"],
        ],
    ),
    # 3. Mild Digestive / Stomach Upset / Nausea
    CuratedConditionPattern(
        key="digestive_mild",
        keywords=[
            "stomach ache",
            "upset stomach",
            "mild nausea",
            "bloating",
            "cramps",
            "indigestion",
            "gas",
            "வயிற்று வலி",
            "வயிறு உப்பசம்",
            "செரிமானமின்மை",
            "vayiru vali",
        ],
        urgency=UrgencyLevel.SELF_CARE_MONITOR,
        signals_en=[
            ObservedSignal(
                label="Gastrointestinal Discomfort",
                description="Mild abdominal discomfort or digestive disturbance without red flags such as severe localized acute pain or vomiting blood.",
            )
        ],
        signals_ta=[
            ObservedSignal(
                label="இரைப்பை குடல் அசௌகரியம்",
                description="கடுமையான ரத்தப்போக்கு அல்லது தீவிர வலி இன்றி ஏற்படும் மிதமான வயிற்று அசௌகரியம்.",
            )
        ],
        explanations_en=[
            PossibleExplanation(
                title="Functional Dyspepsia or Dietary Indigestion",
                description="Common after heavy, spicy, or unfamiliar meals, or eating too rapidly.",
                educational_context="Temporary digestive imbalance that usually self-resolves within 24 to 48 hours.",
            ),
            PossibleExplanation(
                title="Mild Viral Gastroenteritis",
                description="Mild gastrointestinal inflammation often resolving with fluid replenishment.",
                educational_context="Often referred to as stomach bug; maintaining hydration and electrolyte balance is vital.",
            ),
        ],
        explanations_ta=[
            PossibleExplanation(
                title="செரிமானக் கோளாறு (Indigestion / Dyspepsia)",
                description="எண்ணெய், காரமான உணவுகள் அல்லது ஒழுங்கற்ற உணவு நேரங்களால் ஏற்படக்கூடிய மிதமான வயிற்று உபாதை.",
                educational_context="இது பெரும்பாலும் 24 முதல் 48 மணி நேரத்திற்குள் இயல்பு நிலைக்குத் திரும்பும்.",
            ),
            PossibleExplanation(
                title="மிதமான இரைப்பை தொற்று (Mild Gastroenteritis)",
                description="நீரிழப்பைத் தடுத்து எளிய திரவ உணவுகளை உட்கொள்வதன் மூலம் குணமாகக்கூடிய எளிய தொற்று.",
                educational_context="நீர் மற்றும் தாது உப்புச் சத்துக்களை சமநிலையில் வைத்திருப்பது முக்கியம்.",
            ),
        ],
        self_care_en=[
            SelfCareAdvice(
                category="Oral Rehydration",
                tip="Sip clear fluids, oral rehydration solutions (ORS), or diluted juices slowly.",
            ),
            SelfCareAdvice(
                category="Dietary Moderation",
                tip="Stick to bland, easy-to-digest foods (rice, oats, bananas, plain toast). Avoid fried or greasy meals.",
            ),
        ],
        self_care_ta=[
            SelfCareAdvice(
                category="திரவ உணவு மற்றும் நீர்ச்சத்து",
                tip="ORS கரைசல், இளநீர் அல்லது சீரகத் தண்ணீரை சிறிது சிறிதாகப் பருகவும்.",
            ),
            SelfCareAdvice(
                category="எளிய உணவு",
                tip="எண்ணெய் பலகாரங்களைத் தவிர்த்து, கஞ்சி, இட்லி, வாழைப்பழம் போன்ற எளிதில் செரிக்கும் உணவுகளை உண்ணவும்.",
            ),
        ],
        next_steps_en=[
            "Monitor hydration; observe urine color (pale yellow is ideal).",
            "Consult a healthcare professional if pain becomes sharp and localized, persists past 48 hours, or is accompanied by high fever.",
            "Seek immediate emergency care if you experience vomiting blood, severe rigid belly, or inability to keep any fluids down for 24 hours.",
        ],
        next_steps_ta=[
            "நீர்ச்சத்தை கண்காணிக்கவும்.",
            "வயிற்று வலி ஒரு குறிப்பிட்ட பகுதியில் கடுமையாக நீடித்தாலோ அல்லது 2 நாட்களுக்கு மேல் தொடர்ந்தாலோ மருத்துவரை அணுகவும்.",
            "வாந்தியில் ரத்தம் வந்தாலோ அல்லது கடுமையான தாங்க முடியாத வயிற்று வலி ஏற்பட்டாலோ உடனே அவசர சிகிச்சை பெறவும்.",
        ],
        sources=[
            CURATED_TRUSTED_SOURCES["medlineplus_general"],
            CURATED_TRUSTED_SOURCES["nhs_general"],
        ],
    ),
]


def match_curated_pattern(text: str, context: Optional[str] = None) -> Optional[CuratedConditionPattern]:
    combined = f"{text} {context or ''}".lower()
    for pattern in CURATED_PATTERNS:
        if pattern.matches(combined):
            return pattern
    return None
