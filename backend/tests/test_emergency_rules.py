import pytest
from backend.app.safety.detector import EmergencyDetector


@pytest.fixture
def detector():
    return EmergencyDetector()


def test_chest_pain_variations(detector):
    samples = [
        "I have severe chest pain that won't go away",
        "crushing chest pressure radiating to my left arm",
        "my chest feels like an elephant is sitting on it",
        "tightness in chest and jaw pain",
        "நெஞ்சு வலி அதிகமாக இருக்கிறது",
        "nenju vali",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect chest emergency in: {s}"
        assert any(m.category == "CHEST_CARDIOVASCULAR" for m in matches)


def test_respiratory_distress_variations(detector):
    samples = [
        "I can't breathe properly and turning blue",
        "struggling to breathe and gasping for air",
        "severe shortness of breath since 20 minutes",
        "suffocating and unable to speak full sentences",
        "மூச்சுத் திணறல் அதிகமாக உள்ளது",
        "moochu thinarel",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect respiratory distress in: {s}"
        assert any(m.category == "RESPIRATORY_DISTRESS" for m in matches)


def test_stroke_neurological_variations(detector):
    samples = [
        "sudden weakness on one side of my body",
        "my mother has facial drooping and slurred speech",
        "one side is paralyzed suddenly",
        "sudden loss of vision in right eye",
        "பக்கவாதம் மற்றும் பேச்சு குழறல்",
        "pakkavatham",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect stroke signs in: {s}"
        assert any(m.category == "STROKE_NEUROLOGICAL" for m in matches)


def test_altered_consciousness_variations(detector):
    samples = [
        "my brother passed out and is unresponsive",
        "he is unconscious and won't wake up",
        "active epileptic seizure and convulsion",
        "sudden confusion and delirious state",
        "சுயநினைவின்றி மயங்கி விழுந்து விட்டார்",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect altered consciousness in: {s}"
        assert any(m.category == "ALTERED_CONSCIOUSNESS" for m in matches)


def test_severe_bleeding_variations(detector):
    samples = [
        "vomiting blood after an injury",
        "coughing up large amounts of blood",
        "bleeding profusely from deep wound",
        "large amount of blood in stool with severe dizziness",
        "ரத்தம் வாந்தி எடுக்கிறார்",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect severe bleeding in: {s}"
        assert any(m.category == "SEVERE_BLEEDING" for m in matches)


def test_anaphylaxis_variations(detector):
    samples = [
        "swelling of the throat and tongue after peanut allergy",
        "throat is closing up and can't get air",
        "severe allergic reaction with trouble breathing",
        "anaphylactic shock symptoms",
        "தீவிர ஒவ்வாமை காரணமாக தொண்டை வீக்கம்",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect anaphylaxis in: {s}"
        assert any(m.category == "ANAPHYLAXIS" for m in matches)


def test_thunderclap_headache(detector):
    samples = [
        "sudden worst headache of my life that peaked instantly",
        "thunderclap headache with stiff neck",
        "வாழ்நாளின் மிகக் கடுமையான தலைவலி",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect thunderclap headache in: {s}"
        assert any(m.category == "THUNDERCLAP_HEADACHE" for m in matches)


def test_poisoning_overdose(detector):
    samples = [
        "child took too many pills by accident",
        "swallowed poison or drank bleach",
        "விஷம் குடித்து விட்டார்",
    ]
    for s in samples:
        matches = detector.scan(s)
        assert len(matches) > 0, f"Failed to detect poisoning in: {s}"
        assert any(m.category == "POISONING_OVERDOSE" for m in matches)


def test_non_emergency_benign_symptoms(detector):
    benign_samples = [
        "mild headache after staring at laptop",
        "slight runny nose and sneezing once or twice",
        "dry cough for two days without breathing difficulty",
        "mild stomach bloating after eating heavy pizza",
    ]
    for s in benign_samples:
        matches = detector.scan(s)
        assert len(matches) == 0, f"False positive detected in benign case: {s}"
