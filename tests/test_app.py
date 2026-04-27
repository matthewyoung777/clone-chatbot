from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient


API_KEY = "test-key"


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test")
    monkeypatch.setenv("CHATBOT_API_KEY", API_KEY)


@pytest.fixture
def client(mock_env):
    # Patch pool and OpenAI clients before app modules are imported
    with patch("psycopg_pool.ConnectionPool"):
        with patch("app.embeddings.OpenAI"):
            with patch("app.queries.OpenAI"):
                from app.main import app
                yield TestClient(app)


def test_wake_requires_api_key(client):
    resp = client.get("/wake")
    assert resp.status_code == 401


def test_wake_returns_ok(client):
    resp = client.get("/wake", headers={"X-API-KEY": API_KEY})
    assert resp.status_code == 200
    assert resp.json() == {"answer": "I'm awake"}


def test_ask_requires_api_key(client):
    resp = client.post("/ask", json={"question": "What do you do?"})
    assert resp.status_code == 401


def test_ask_returns_answer(client):
    with patch("app.main.process_query", return_value="I'm a software engineer."):
        resp = client.post(
            "/ask",
            json={"question": "What do you do?"},
            headers={"X-API-KEY": API_KEY},
        )
    assert resp.status_code == 200
    assert resp.json() == {"answer": "I'm a software engineer."}


def test_ask_missing_question_field(client):
    resp = client.post("/ask", json={}, headers={"X-API-KEY": API_KEY})
    assert resp.status_code == 422


def test_ask_unanswerable_question(client):
    with patch(
        "app.main.process_query", return_value="Sorry I can't answer that."
    ):
        resp = client.post(
            "/ask",
            json={"question": "What is the meaning of life?"},
            headers={"X-API-KEY": API_KEY},
        )
    assert resp.status_code == 200
    assert "can't answer" in resp.json()["answer"]
