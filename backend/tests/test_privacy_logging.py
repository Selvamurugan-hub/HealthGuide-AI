import logging
from starlette.testclient import TestClient


def test_privacy_no_raw_symptom_logging(client: TestClient, caplog):
    caplog.set_level(logging.INFO)

    unique_sensitive_text = "CONFIDENTIAL_PATIENT_SYMPTOM_TOKEN_98765_MILD_COUGH"
    payload = {
        "age_range": "ADULT_18_64",
        "symptoms_text": f"I have a cough and {unique_sensitive_text}",
        "duration": "DAYS_1_TO_3",
        "severity": "MILD",
        "additional_context": "SECRET_CONTEXT_TOKEN_43210",
        "language": "en",
    }

    response = client.post("/api/assess", json=payload)
    assert response.status_code == 200

    # Inspect all logs captured during the request lifecycle
    full_log_text = "\n".join([record.getMessage() for record in caplog.records])

    # Asserts that neither the secret symptom text nor additional context was printed into logs
    assert unique_sensitive_text not in full_log_text, "Privacy breach: raw symptom description found in log output!"
    assert "SECRET_CONTEXT_TOKEN_43210" not in full_log_text, "Privacy breach: additional context found in log output!"
