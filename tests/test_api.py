import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "AgentPulse" in data["service"]


def test_root_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "AgentPulse" in response.text


def test_research_api_flow():
    payload = {
        "query": "SQLite vs DuckDB for analytics",
        "depth": "standard",
        "domain_filter": "engineering"
    }
    response = client.post("/api/research", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data
    assert "evidence_gathered" in data
    assert "final_report" in data
    assert data["final_report"]["confidence_score"] > 0.0

    history_resp = client.get("/api/history")
    assert history_resp.status_code == 200
    history_items = history_resp.json()
    assert len(history_items) >= 1

