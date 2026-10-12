from starlette.testclient import TestClient


def test_tamil_emergency_assessment(client: TestClient):
    payload = {
        "age_range": "ADULT_18_64",
        "symptoms_text": "நெஞ்சு வலி மிக அதிகமாக இருக்கிறது மூச்சு விட முடியவில்லை",
        "duration": "LESS_THAN_24_HOURS",
        "severity": "CRITICAL",
        "language": "ta",
    }
    response = client.post("/api/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "ta"
    assert data["urgency_level"] == "EMERGENCY"
    assert data["is_emergency"] is True
    assert "அவசர" in data["emergency_notice"]["title"]
    assert "108" in str(data["emergency_notice"]["emergency_numbers"])
    assert len(data["next_steps"]) > 0
    # Next steps must contain Tamil text
    assert any("அவசர" in step for step in data["next_steps"])


def test_tamil_routine_curated_assessment(client: TestClient):
    payload = {
        "age_range": "ADULT_18_64",
        "symptoms_text": "லேசான தலைவலி உள்ளது இரண்டு நாட்களாக",
        "duration": "DAYS_1_TO_3",
        "severity": "MILD",
        "language": "ta",
    }
    response = client.post("/api/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "ta"
    assert data["is_emergency"] is False
    assert len(data["possible_explanations"]) > 0
    assert "தலைவலி" in data["possible_explanations"][0]["title"]
    assert len(data["self_care_guidance"]) > 0
