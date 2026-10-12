import re
from typing import Dict, List, Pattern

class EmergencyRule:
    def __init__(
        self,
        category: str,
        name_en: str,
        name_ta: str,
        description_en: str,
        description_ta: str,
        patterns: List[str],
    ):
        self.category = category
        self.name_en = name_en
        self.name_ta = name_ta
        self.description_en = description_en
        self.description_ta = description_ta
        # Compile patterns with case-insensitivity
        self.compiled_patterns: List[Pattern] = [
            re.compile(p, re.IGNORECASE) for p in patterns
        ]


EMERGENCY_RULES: List[EmergencyRule] = [
    EmergencyRule(
        category="CHEST_CARDIOVASCULAR",
        name_en="Severe Chest Pain or Cardiac Symptoms",
        name_ta="கடுமையான மார்பு வலி அல்லது இதய அவசர அறிகுறிகள்",
        description_en="Possible acute cardiovascular crisis requiring immediate emergency evaluation.",
        description_ta="உடனடி அவசர மருத்துவ சிகிச்சை தேவைப்படும் இதயக் கோளாறுக்கான சாத்தியமான அறிகுறிகள்.",
        patterns=[
            r"\b(chest\s+pain|chest\s+tightness|chest\s+pressure|crushing\s+chest|squeezing\s+chest|heavy\s+chest)\b",
            r"\b(tightness|pressure|heaviness|pain)\s+in\s+(my\s+)?chest\b",
            r"\b(pain\s+(radiating|spreading)\s+to\s+(left\s+)?(arm|jaw|neck|back))\b",
            r"\b(heart\s+attack|angina|cardiac\s+arrest)\b",
            r"\bchest\s+feels\s+(heavy|tight|like\s+an\s+elephant)\b",
            # Tamil keywords & transliterations
            r"மார்பு\s*வலி|நெஞ்சு\s*வலி|நெஞ்சு\s*அடைப்ப|நெஞ்சில்\s*பாரம்",
            r"\b(nenju\s+vali|marbu\s+vali|nenjil\s+param)\b",
        ],
    ),
    EmergencyRule(
        category="RESPIRATORY_DISTRESS",
        name_en="Severe Breathing Difficulty or Airway Compromise",
        name_ta="கடுமையான மூச்சுத் திணறல் அல்லது சுவாசக் கோளாறு",
        description_en="Acute shortage of oxygen or airway obstruction.",
        description_ta="ஆக்ஸிஜன் பற்றாக்குறை அல்லது சுவாசப்பாதை அடைப்புக்கான அவசர அறிகுறிகள்.",
        patterns=[
            r"\b(can'?t\s+breathe|cannot\s+breathe|unable\s+to\s+breathe|struggling\s+to\s+breathe)\b",
            r"\b(gasping\s+for\s+(air|breath)|shortness\s+of\s+breath|severe\s+breathlessness)\b",
            r"\b(suffocating|choking|air\s+hunger|turning\s+blue|cyanosis)\b",
            r"\b(can'?t\s+get\s+enough\s+air|hard\s+to\s+catch\s+my\s+breath)\b",
            r"\b(wheezing\s+severely|stridor)\b",
            # Tamil keywords & transliterations
            r"மூச்சுத்\s*திணறல்|மூச்சு\s*விட\s*முடியவில்லை|மூச்சு\s*வாங்க\s*முடியல|சுவாசிக்க\s*முடியவில்லை",
            r"\b(moochu\s+thinarel|moochu\s+vida\s+mudiyala)\b",
        ],
    ),
    EmergencyRule(
        category="STROKE_NEUROLOGICAL",
        name_en="Sudden Stroke or Neurological Deficit",
        name_ta="திடீர் பக்கவாதம் அல்லது நரம்பியல் குறைபாடு",
        description_en="Sudden neurological signs (FAST: Face, Arms, Speech, Time) warranting emergency stroke protocol.",
        description_ta="உடனடி அவசர சிகிச்சை தேவைப்படும் பக்கவாத அறிகுறிகள் (முகம், கை தளர்ச்சி, பேச்சு தடுமாற்றம்).",
        patterns=[
            r"\b(stroke|mini[- ]stroke|tia)\b",
            r"\b(facial\s+droop(ing)?|face\s+is\s+drooping|drooping\s+face)\b",
            r"\b(slurred\s+speech|slurring\s+words|cannot\s+speak|unable\s+to\s+talk)\b",
            r"\b(sudden\s+weakness\s+(in|on)\s+one\s+side|one\s+side\s+(is\s+)?paralyzed|numbness\s+on\s+one\s+side)\b",
            r"\b(sudden\s+loss\s+of\s+vision|sudden\s+blindness)\b",
            r"\b(paralysis|hemiplegia)\b",
            # Tamil keywords
            r"பக்கவாதம்|முகம்\s*கோணல்|பேச்சு\s*குழறல்|ஒரு\s*பக்கம்\s*செயலிழப்பு",
            r"\b(pakkavatham|pechu\s+kuzharal)\b",
        ],
    ),
    EmergencyRule(
        category="ALTERED_CONSCIOUSNESS",
        name_en="Unconsciousness, Unresponsiveness, or Syncope",
        name_ta="சுயநினைவின்மை அல்லது மயக்கம்",
        description_en="Significant impairment or loss of consciousness or unresponsiveness.",
        description_ta="சுயநினைவு இழப்பு அல்லது விழிப்புணர்வு அற்ற அவசர நிலை.",
        patterns=[
            r"\b(unconscious|passed\s+out|lost\s+consciousness|blacked\s+out|unresponsive)\b",
            r"\b(won'?t\s+wake\s+up|cannot\s+wake\s+(him|her|them|up))\b",
            r"\b(seizure|convulsions|fitting|epileptic\s+fit)\b",
            r"\b(sudden\s+confusion|disoriented\s+and\s+confused|delirious)\b",
            # Tamil keywords
            r"சுயநினைவின்றி|மயக்கம்\s*அடைந்து|மயங்கி\s*விழுந்து|வலிப்பு",
            r"\b(mayakkam|suyaninaivindri|valippu)\b",
        ],
    ),
    EmergencyRule(
        category="SEVERE_BLEEDING",
        name_en="Severe or Uncontrolled Hemorrhage",
        name_ta="கடுமையான அல்லது நிற்காத ரத்தப்போக்கு",
        description_en="Rapid blood loss that can lead to hypovolemic shock.",
        description_ta="அதிர்ச்சிக்கு வழிவகுக்கும் தீவிர ரத்த இழப்பு.",
        patterns=[
            r"\b(vomiting\s+blood|throwing\s+up\s+blood|hematemesis)\b",
            r"\b(coughing\s+up\s+.*?\bblood\b|coughing\s+up\s+blood|hemoptysis)\b",
            r"\b(bleeding\s+profusely|uncontrolled\s+bleeding|severe\s+bleeding|gushing\s+blood)\b",
            r"\b(large\s+amount\s+of\s+blood\s+in\s+stool|black\s+tarry\s+stool)\b",
            # Tamil keywords
            r"ரத்தம்\s*வாந்தி|ரத்தப்போக்கு|கடுமையான\s*ரத்தம்",
            r"\b(ratham\s+vanthi|rathapokku)\b",
        ],
    ),
    EmergencyRule(
        category="ANAPHYLAXIS",
        name_en="Severe Allergic Reaction (Anaphylaxis)",
        name_ta="தீவிர ஒவ்வாமை (அனாபிலாக்ஸிஸ்)",
        description_en="Systemic severe allergic response impacting airways or blood pressure.",
        description_ta="சுவாசப்பாதை அல்லது ரத்த அழுத்தத்தை பாதிக்கும் கடுமையான ஒவ்வாமை.",
        patterns=[
            r"\b(anaphylaxis|anaphylactic\s+shock)\b",
            r"\b(swelling\s+of\s+(the\s+)?(throat|tongue|lips)|throat\s+(is\s+)?closing(\s+up)?)\b",
            r"\b(allergic\s+reaction\s+with\s+(trouble\s+breathing|swelling))\b",
            r"\b(swollen\s+airway|throat\s+is\s+swelling)\b",
            # Tamil keywords
            r"தீவிர\s*ஒவ்வாமை|தொண்டை\s*வீக்கம்|நாக்கு\s*வீக்கம்",
            r"\b(theevira\s+ovvaamai|thondai\s+veekkam)\b",
        ],
    ),
    EmergencyRule(
        category="THUNDERCLAP_HEADACHE",
        name_en="Sudden Severe 'Thunderclap' Headache",
        name_ta="திடீர் அதிதீவிர தலைவலி (தண்டர்கிளாப்)",
        description_en="Sudden, explosive headache reaching maximum intensity in seconds to minutes, possible subarachnoid hemorrhage.",
        description_ta="நொடிகளில் உச்சக்கட்டத்தை எட்டும் வெடிக்கும் வகைத் தலைவலி.",
        patterns=[
            r"\b(thunderclap\s+headache|worst\s+headache\s+of\s+my\s+life|worst\s+headache\s+ever)\b",
            r"\b(sudden\s+severe\s+headache|explosive\s+headache)\b",
            r"\b(headache\s+with\s+stiff\s+neck\s+and\s+fever)\b",
            # Tamil keywords
            r"வாழ்நாளின்\s*மிகக்\s*கடுமையான\s*தலைவலி|திடீர்\s*வெடிக்கும்\s*தலைவலி",
        ],
    ),
    EmergencyRule(
        category="POISONING_OVERDOSE",
        name_en="Suspected Poisoning, Toxicity, or Overdose",
        name_ta="நச்சு உட்கொள்ளல் அல்லது மருந்து அளவுக்கதிகம்",
        description_en="Accidental or intentional ingestion of dangerous toxic substances or medication overdose.",
        description_ta="நச்சுப் பொருட்கள் அல்லது மருந்துகளை அளவுக்கு அதிகமாக உட்கொண்ட அவசர நிலை.",
        patterns=[
            r"\b(overdose|swallowed\s+poison|drank\s+bleach|ingested\s+chemical)\b",
            r"\b(poisoning|toxic\s+ingestion|drank\s+pesticide)\b",
            r"\b(took\s+too\s+many\s+pills|swallowed\s+battery)\b",
            # Tamil keywords
            r"விஷம்\s*குடித்து|நஞ்சு|மருந்து\s*அளவுக்கதிகம்",
            r"\b(visham|nanju)\b",
        ],
    ),
]
