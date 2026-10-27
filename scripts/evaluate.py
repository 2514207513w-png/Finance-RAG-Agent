"""Deterministic offline smoke evaluation; not a statistical benchmark."""
import json
from pathlib import Path
from finance_agent.factory import build_agent

def main():
    cases=[json.loads(s) for s in (Path(__file__).resolve().parents[1]/"data/eval_cases.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    agent=build_agent()
    ok=0
    for i,c in enumerate(cases):
        actual=agent.ask(c["question"],f"evaluation-{i}")
        passed=(actual["intent"]==c["expected_intent"] and actual["active_product"]==c["expected_product"] and (not c.get("require_source") or bool(actual["sources"])))
        print("PASS" if passed else "FAIL",c["question"],"->",actual["intent"],actual["active_product"])
        ok+=passed
    print(f"Workflow smoke checks: {ok}/{len(cases)} passed; not evidence of answer quality or LLM accuracy")
    if ok!=len(cases): raise SystemExit(1)

if __name__=="__main__":main()
