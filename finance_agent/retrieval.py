"""FAISS cosine similarity (normalized vectors) + product filtering.
Hash mode is intentionally NOT a semantic encoder; use sentence mode for meaning.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np

class HashedEmbeddings:
    """A deterministic character n-gram baseline for offline smoke tests."""
    def __init__(self, dim: int = 384): self.dim=dim
    def encode(self, texts: list[str]) -> np.ndarray:
        rows=[]
        for s in texts:
            text=s.lower()
            grams=list(text)+[text[i:i+2] for i in range(len(text)-1)]
            vector=np.zeros(self.dim,dtype=np.float32)
            for gram in grams:
                digest=hashlib.sha256(gram.encode("utf-8")).digest()
                vector[int.from_bytes(digest[:4],"little") % self.dim]+=1
            norm=float(np.linalg.norm(vector))
            if norm: vector/=norm
            rows.append(vector)
        return np.stack(rows) if rows else np.empty((0,self.dim),dtype=np.float32)

class SentenceEmbeddings:
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise RuntimeError("Install semantic embeddings: pip install -e '.[semantic]'") from e
        self.encoder=SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    def encode(self,texts:list[str])->np.ndarray:
        return np.asarray(self.encoder.encode(texts, normalize_embeddings=True),dtype=np.float32)

class DocumentRetriever:
    def __init__(self, chunks: list[dict], embedder=None, use_faiss=True):
        self.chunks=chunks
        self.embedder=embedder or HashedEmbeddings()
        self.vectors=self.embedder.encode([c["text"] for c in chunks])
        self.index=None
        if self.vectors.size and use_faiss:
            try:
                import faiss
                self.index=faiss.IndexFlatIP(self.vectors.shape[1])
                self.index.add(self.vectors)
            except ImportError:
                pass  # numpy fallback enables offline utility tests

    def search(self, query: str, product_codes: list[str] | None=None, k: int=3) -> list[dict]:
        if not self.chunks or k < 1: return []
        needle=self.embedder.encode([query])
        if self.index is not None:
            scores, idx=self.index.search(needle, len(self.chunks))
            ranked=list(zip(idx[0].tolist(),scores[0].tolist()))
        else:
            similarity=(self.vectors @ needle[0]).tolist()
            ranked=sorted(enumerate(similarity), key=lambda z:z[1],reverse=True)
        allowed={p.upper() for p in product_codes} if product_codes else None
        matches=[]
        for idx,score in ranked:
            c=self.chunks[idx]
            if allowed is not None and c.get("product_code","").upper() not in allowed: continue
            matches.append({**c,"score":round(float(score),5)})
            if len(matches)>=k:break
        return matches

def load_chunks(path: str | Path) -> list[dict]:
    p=Path(path)
    return json.loads(p.read_text(encoding="utf-8"))
