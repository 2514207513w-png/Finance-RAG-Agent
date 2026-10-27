"""FastAPI demo, local-only by default. No auth; do not expose publicly."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .factory import build_agent

app=FastAPI(title="Finance RAG Agent (Synthetic Demo)",version="0.2.0")

class AskRequest(BaseModel):
    thread_id: str = Field(min_length=1,max_length=128,pattern=r"^[A-Za-z0-9_-]+$")
    question: str = Field(min_length=1,max_length=3000)

class AskResponse(BaseModel):
    answer: str
    intent: str
    active_product: str
    sources: list[str]

@app.get("/health")
def health(): return {"status":"ok","mode":"demo"}

@app.post("/api/v1/ask",response_model=AskResponse)
def ask(body:AskRequest):
    try:
        return build_agent().ask(body.question,body.thread_id)
    except (ValueError,RuntimeError) as exc:
        raise HTTPException(status_code=503,detail=str(exc)) from exc
