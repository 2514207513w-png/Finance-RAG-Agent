"""Deterministic fallback router for offline, no-key reproducibility."""
import re
from dataclasses import dataclass
from typing import Literal

CODE_RE = re.compile(r"DEMO\d{3}", re.IGNORECASE)
Intent = Literal["product_info", "compare_products", "document_qa"]

@dataclass(frozen=True)
class ToolPlan:
    intent: Intent
    product_codes: list[str]


def plan_question(question: str, active_product: str | None = None) -> ToolPlan:
    explicit = list(dict.fromkeys(x.upper() for x in CODE_RE.findall(question)))
    if ("比较" in question or "相比" in question or "对比" in question) and len(explicit) >= 2:
        return ToolPlan("compare_products", explicit[:2])
    if ("比较" in question or "相比" in question or "对比" in question) and len(explicit)==1 and active_product and active_product.upper()!=explicit[0]:
        return ToolPlan("compare_products", [active_product.upper(),explicit[0]])
    codes = explicit if explicit else ([active_product.upper()] if active_product else [])
    if any(x in question for x in ("风险等级", "基本信息", "产品名称", "风险级别")):
        return ToolPlan("product_info", codes[:1])
    return ToolPlan("document_qa", codes[:1])
