# API examples

Start: `uvicorn finance_agent.api:app --reload --port 8010`

Swagger UI: `http://127.0.0.1:8010/docs`

```bash
curl http://127.0.0.1:8010/health
curl -X POST http://127.0.0.1:8010/api/v1/ask -H 'Content-Type: application/json' -d '{"thread_id":"demo","question":"DEMO001风险等级是什么？"}'
curl -X POST http://127.0.0.1:8010/api/v1/ask -H 'Content-Type: application/json' -d '{"thread_id":"demo","question":"它的赎回规则是什么？"}'
```

This is a **local demo**, not an authenticated public service.
