from functools import lru_cache
from pathlib import Path
from .settings import Settings
from .store import APIProductStore,SampleProductStore
from .retrieval import DocumentRetriever, HashedEmbeddings,SentenceEmbeddings,load_chunks

@lru_cache(maxsize=1)
def build_agent():
    from .graph import FinanceAgent
    cfg=Settings.from_env()
    store=(APIProductStore(cfg.findatahub_base_url,cfg.findatahub_token)
        if cfg.backend_mode=="api" else SampleProductStore())
    embedder=SentenceEmbeddings() if cfg.embedding_mode=="sentence" else HashedEmbeddings()
    chunks=load_chunks(Path(__file__).resolve().parents[1]/"data"/"chunks.json")
    retriever=DocumentRetriever(chunks,embedder)
    llm=None
    if cfg.agent_mode=="llm":
        from .llm import ChatAPI
        llm=ChatAPI(cfg.openai_api_base,cfg.openai_api_key,cfg.openai_model)
    return FinanceAgent(store,retriever,llm)
