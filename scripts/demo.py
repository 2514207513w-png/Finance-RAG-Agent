from finance_agent.factory import build_agent

a=build_agent()
for q in ("DEMO001 的风险等级是什么？", "它的赎回规则是什么？", "比较 DEMO001 和 DEMO002 的风险等级"):
    print("\n用户：",q)
    print("Agent：",a.ask(q,"quickstart")['answer'])
