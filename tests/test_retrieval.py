from finance_agent.retrieval import DocumentRetriever,HashedEmbeddings

def test_embedding_deterministic():
    e=HashedEmbeddings()
    assert (e.encode(["同一段文字"])==e.encode(["同一段文字"])).all()

def test_product_filter():
    chunks=[{"product_code":"DEMO001","document_id":"d1","page":1,"text":"赎回规则测试"}, {"product_code":"DEMO002","document_id":"d2","page":2,"text":"赎回规则测试"}]
    r=DocumentRetriever(chunks, use_faiss=False)
    hits=r.search("赎回规则测试",["DEMO002"])
    assert hits and all(x["product_code"]=="DEMO002" for x in hits)
