from starlette.testclient import TestClient


def test_valid_routine_symptom_assessment(client: TestClient):
    payload = {
        "age_range": "ADULT_18_64",
        "symptoms_text": "I have had a mild tension headache for 2 days after working on computer screens.",
        "duration": "DAYS_1_TO_3",
        "severity": "MILD",
        "additional_context": "No fever or vision changes.",
        "language": "en",
    }
    response = client.post("/api/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency_level"] == "SELF_CARE_MONITOR"
    assert data["is_emergency"] is False
    assert data["emergency_notice"] is None
    assert len(data["possible_explanations"]) > 0
    assert len(data["trusted_sources"]) > 0
    # Ensure no fabricated percentage or diagnosis claim
    for exp in data["possible_explanations"]:
        assert "%" not in exp["title"]
        assert "probability" not in exp["title"].lower()
    assert "not a diagnosis" in data["disclaimer"].lower()


def test_empty_and_whitespace_symptoms_rejected(client: TestClient):
    # Empty string
    res_empty = client.post(
        "/api/assess",
        json={
            "age_range": "ADULT_18_64",
            "symptoms_text": "",
            "duration": "DAYS_1_TO_3",
            "severity": "MILD",
        },
    )
    assert res_empty.status_code == 422

    # Whitespace only
    res_ws = client.post(
        "/api/assess",
        json={
            "age_range": "ADULT_18_64",
            "symptoms_text": "     ",
            "duration": "DAYS_1_TO_3",
            "severity": "MILD",
        },
    )
    assert res_ws.status_code == 422


def test_excessively_long_symptoms_rejected(client: TestClient):
    too_long = "pain " * 400  # 2000 characters > 1500 limit
    res_long = client.post(
        "/api/assess",
        json={
            "age_range": "ADULT_18_64",
            "symptoms_text": too_long,
            "duration": "DAYS_1_TO_3",
            "severity": "MILD",
        },
    )
    assert res_long.status_code == 422


def test_invalid_age_range_rejected(client: TestClient):
    res = client.post(
        "/api/assess",
        json={
            "age_range": "INVALID_AGE",
            "symptoms_text": "Mild headache",
            "duration": "DAYS_1_TO_3",
            "severity": "MILD",
        },
    )
    assert res.status_code == 422


def test_ambiguous_symptoms_handling(client: TestClient):
    payload = {
        "age_range": "ADULT_18_64",
        "symptoms_text": "My ear feels slightly buzzing and weird sensation when I chew gum.",
        "duration": "DAYS_4_TO_7",
        "severity": "MILD",
        "language": "en",
    }
    response = client.post("/api/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency_level"] == "AMBIGUOUS_CONSULT_CLINICIAN"
    assert data["is_emergency"] is False
    assert "uncertainty_notice" in data
    # Must advise seeing clinician rather than fabricating diagnosis
    assert any("consult" in step.lower() or "provider" in step.lower() or "doctor" in step.lower() for step in data["next_steps"])
