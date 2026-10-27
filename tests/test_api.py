import pytest
pytest.importorskip("langgraph")
from fastapi.testclient import TestClient
from finance_agent.api import app

def test_health_and_ask(monkeypatch):
    monkeypatch.setenv("AGENT_MODE","offline")
    monkeypatch.setenv("BACKEND_MODE","sample")
    from finance_agent.factory import build_agent
    build_agent.cache_clear()
    with TestClient(app) as client:
        assert client.get("/health").status_code==200
        res=client.post("/api/v1/ask",json={"thread_id":"api-test","question":"DEMO001风险等级是什么"})
        assert res.status_code==200
        assert res.json()["sources"]
