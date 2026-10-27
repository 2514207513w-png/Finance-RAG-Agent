"""LangGraph application. Sample/offline runs without an external model."""
from __future__ import annotations
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from .router import plan_question
from .retrieval import DocumentRetriever

class AgentState(TypedDict, total=False):
    question: str
    active_product: str
    intent: str
    product_codes: list[str]
    evidence: list[dict]
    answer: str
    error: str

class FinanceAgent:
    def __init__(self, store, retriever: DocumentRetriever, llm=None):
        self.store=store
        self.retriever=retriever
        self.llm=llm
        self.graph=self._make_graph()

    def _make_graph(self):
        def route(state:AgentState):
            if self.llm:
                plan=self.llm.select(state["question"],state.get("active_product"))
            else:
                plan=plan_question(state["question"],state.get("active_product"))
            product_codes=[p for p in plan.product_codes if p and p.isalnum() and len(p)<=40]
            active=product_codes[-1] if product_codes else state.get("active_product","")
            return {"intent":plan.intent,"product_codes":product_codes,"active_product":active,"evidence":[],"answer":"","error":""}

        def product_info(state:AgentState):
            evidence=[]
            for code in state.get("product_codes",[]):
                try:
                    value=self.store.get(code)
                except Exception as e:
                    return {"evidence":[],"error":f"后端接口暂不可用：{type(e).__name__}"}
                if value:
                    fields={"code":value.get("code"),"name":value.get("name"),"risk_level":value.get("risk_level"),"source_url":value.get("source_url")}
                    evidence.append({"source":f"product-api:{code}","text":str(fields)})
            return {"evidence":evidence}

        def document_qa(state:AgentState):
            codes=state.get("product_codes") or []
            if not codes:
                return {"evidence":[],"error":"请先提供要查询的产品代码。"}
            chunks=self.retriever.search(state["question"],product_codes=codes,k=3)
            evidence=[{"source":f"{c['document_id']}#page={c.get('page','?')}","text":c["text"]} for c in chunks]
            return {"evidence":evidence}

        def render(state:AgentState):
            ev=state.get("evidence",[])
            if not ev:
                return {"answer":state.get("error") or "当前未检索到能够核实的产品信息，请补充产品代码或文档。"}
            if self.llm:
                body=self.llm.answer(state["question"],ev)
            else:
                body="离线演示模式：以下为检索证据，并非模型推理生成的结论。"
                body+="\n"+"\n".join(f"• {x['text']}" for x in ev)
            sources="；".join(dict.fromkeys(x["source"] for x in ev))
            return {"answer":body+"\n来源："+sources}

        b=StateGraph(AgentState)
        for name, fn in (("route",route),("product_info",product_info),("document_qa",document_qa),("render",render)):
            b.add_node(name,fn)
        b.add_edge(START,"route")
        b.add_conditional_edges("route",lambda s:s["intent"],{"product_info":"product_info","compare_products":"product_info","document_qa":"document_qa"})
        b.add_edge("product_info","render")
        b.add_edge("document_qa","render")
        b.add_edge("render",END)
        return b.compile(checkpointer=InMemorySaver())

    def ask(self, question: str, thread_id: str):
        result=self.graph.invoke({"question":question},config={"configurable":{"thread_id":thread_id}})
        return {"answer":result["answer"],"intent":result["intent"],"active_product":result.get("active_product",""),"sources":list(dict.fromkeys(x["source"] for x in result.get("evidence",[])))}
