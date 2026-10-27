from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Settings:
    agent_mode: str = "offline"
    backend_mode: str = "sample"
    embedding_mode: str = "hash"
    openai_api_base: str = ""
    openai_api_key: str = ""
    openai_model: str = ""
    findatahub_base_url: str = "http://127.0.0.1:8000"
    findatahub_token: str = ""

    @classmethod
    def from_env(cls):
        result = cls(
            agent_mode=os.getenv("AGENT_MODE", "offline"),
            backend_mode=os.getenv("BACKEND_MODE", "sample"),
            embedding_mode=os.getenv("EMBEDDING_MODE", "hash"),
            openai_api_base=os.getenv("OPENAI_API_BASE", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", ""),
            findatahub_base_url=os.getenv("FINDATAHUB_BASE_URL", "http://127.0.0.1:8000"),
            findatahub_token=os.getenv("FINDATAHUB_TOKEN", ""),
        )
        if result.agent_mode not in ("offline", "llm"):
            raise ValueError("AGENT_MODE must be offline or llm")
        if result.backend_mode not in ("sample", "api"):
            raise ValueError("BACKEND_MODE must be sample or api")
        if result.embedding_mode not in ("hash", "sentence"):
            raise ValueError("EMBEDDING_MODE must be hash or sentence")
        if result.agent_mode == "llm" and not all((result.openai_api_base, result.openai_api_key, result.openai_model)):
            raise ValueError("LLM mode requires OPENAI_API_BASE, OPENAI_API_KEY, OPENAI_MODEL")
        return result
