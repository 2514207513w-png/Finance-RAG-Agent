import pytest
pytest.importorskip("langgraph")
from finance_agent.graph import FinanceAgent
from finance_agent.store import SampleProductStore
from finance_agent.retrieval import DocumentRetriever,load_chunks
from pathlib import Path

def test_multiturn_and_thread_isolation():
    chunks=load_chunks(Path(__file__).resolve().parents[1]/"data"/"chunks.json")
    agent=FinanceAgent(SampleProductStore(),DocumentRetriever(chunks,use_faiss=False))
    a=agent.ask("DEMO001的风险等级是什么？","thread1")
    b=agent.ask("它的赎回规则是什么？","thread1")
    c=agent.ask("它的赎回规则是什么？","thread2")
    assert a["intent"]=="product_info"
    assert b["active_product"]=="DEMO001" and b["sources"]
    assert not c["sources"]

def test_compare_two_products():
    chunks=load_chunks(Path(__file__).resolve().parents[1]/"data"/"chunks.json")
    agent=FinanceAgent(SampleProductStore(),DocumentRetriever(chunks,use_faiss=False))
    actual=agent.ask("比较DEMO001和DEMO002的风险等级","comparison")
    assert len(actual["sources"])==2
