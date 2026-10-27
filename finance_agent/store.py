"""Read-only synthetic products used when BACKEND_MODE=sample."""
import json
from pathlib import Path
from typing import Any

DATA = Path(__file__).resolve().parents[1]/"data"

class SampleProductStore:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else DATA / "products.json"
        values = json.loads(self.path.read_text(encoding="utf-8"))
        self.items = {v["code"].upper(): v for v in values}

    def get(self, code: str) -> dict[str, Any] | None:
        return self.items.get(code.upper())

class APIProductStore:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def get(self, code: str) -> dict | None:
        import httpx
        # Only synthetic alphanumeric codes accepted; model-supplied arbitrary URLs are prohibited.
        if not code.isalnum() or len(code) > 40:
            raise ValueError("invalid product code")
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        with httpx.Client(timeout=10) as client:
            response = client.get(f"{self.base_url}/api/v1/products/{code}", headers=headers)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
