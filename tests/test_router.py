from finance_agent.router import plan_question

def test_basic_route():
    result=plan_question("DEMO001的风险等级是什么")
    assert result.intent=="product_info"
    assert result.product_codes==["DEMO001"]

def test_followup_product():
    result=plan_question("它的赎回规则是什么", "DEMO001")
    assert result.intent=="document_qa"
    assert result.product_codes==["DEMO001"]

def test_compare_two():
    result=plan_question("比较DEMO001和DEMO002的风险等级")
    assert result.intent=="compare_products"
    assert result.product_codes==["DEMO001","DEMO002"]
