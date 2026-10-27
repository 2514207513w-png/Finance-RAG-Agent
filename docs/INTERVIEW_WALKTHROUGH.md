# Interview walkthrough / 项目面试逻辑

Use only after running and testing what you claim.

1. **Problem**: product attributes are structured; disclosures and redemption clauses are unstructured. Do not trust LLM memory for latest terms.
2. **Data layer**: test product store or FinDataHub API; PDF chunks with product/document/page metadata.
3. **State machine**: LangGraph `route -> product_info/document_qa -> render`; per-thread active product checkpoint.
4. **Search**: offline hash-vector for smoke testing, optional multilingual semantic model; normalize embedding and FAISS IP search. Filter product codes to prevent cross-product results.
5. **Grounding**: each returned evidence has a source id; no evidence -> explicit no-answer.
6. **Trace/metrics**: evaluator checks deterministic route and source presence, **not** model answer correctness, citation faithfulness or production precision.
7. **Failure**: unknown product, missing context, backend HTTP errors, unavailable model tool_calls, no scanned-PDF OCR, non-persistent session state.

**Technical follow-ups**: How is State updated? What is the difference between checkpoint and long-term Memory? When does cache consistency belong to backend rather than Agent? Why use a Tool API instead of direct SQL? What if source docs are outdated? How to test hallucinations and cross-user leakage?

**Honesty**: the included source is a learning/demo starter. Claim only original modifications, experiments and integrations you actually completed.
