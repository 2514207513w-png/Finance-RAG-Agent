# Finance RAG Agent | 基于 LangGraph 的金融知识 RAG 与多轮问答

**作品展示用学习项目 / Reproducible portfolio starter (synthetic data).**

## 实现范围

- ✅ LangGraph `StateGraph` 与 `InMemorySaver` 会话状态
- ✅ 产品属性查询工具与按产品范围的文档检索路径
- ✅ FAISS 向量检索（语义模型可选；默认无 Key 模式使用字符串哈希向量，仅做逻辑验证）
- ✅ 多轮产品指代（同一 `thread_id`）；不同线程不共享活动产品
- ✅ FastAPI Swagger 接口、合成数据、基础单元测试与评测脚本
- ✅ 可选 FinDataHub 产品查询 API 接入
- ⚙️ 可选调用支持 `tool_calls` 的 OpenAI-compatible LLM（需个人授权的 API 及 Key）
- ⚠️ 默认**无 LLM 生成**；离线回答只是原始证据展示，不是金融投顾或经验证的问答模型
- ⚠️ 未实现线上多用户身份隔离、持久化会话、复杂自主规划和生产级引用忠实度评测

## 快速启动（Python 3.11，Windows/macOS/Linux）

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m scripts.demo
python -m pytest -q
python -m uvicorn finance_agent.api:app --reload --port 8010
```

打开 http://127.0.0.1:8010/docs，调用 `POST /api/v1/ask`：

```json
{"thread_id":"demo-001","question":"DEMO001的风险等级是什么？"}
```

再次以同一个 `thread_id` 提问：

```json
{"thread_id":"demo-001","question":"它的赎回规则是什么？"}
```

你还可以运行：`python -m scripts.evaluate` 查看 5 个小规模的工作流 Smoke Cases。
如果尚未安装依赖，只运行 `python -m scripts.check_package` 验证源码与 JSON 可正常读取。

Windows 更详细步骤：[`docs/WINDOWS_QUICKSTART.md`](docs/WINDOWS_QUICKSTART.md)。

## 两种模式

| 配置 | 默认值 | 说明 |
|---|---|---|
| `AGENT_MODE` | `offline` | 离线规则路由 + 证据拼接；`llm` 使用工具调用和生成（必须提供模型配置） |
| `BACKEND_MODE` | `sample` | 本地 `data/products.json`；`api` 调用独立 FinDataHub REST API |
| `EMBEDDING_MODE` | `hash` | 离线字符串向量；`sentence` 使用多语言 SentenceTransformer（需另装依赖并下载模型） |

使用 `cp .env.example .env`（Windows 使用 `Copy-Item`），然后编辑 `.env`。

语义检索安装：

```bash
python -m pip install -e '.[semantic]'
```

连接 FinDataHub 后端时，设为 `BACKEND_MODE=api`，配置 `FINDATAHUB_BASE_URL` 与该服务的授权 Token。请先启动 FinDataHub。当前演示文档索引仍来自本地 `data/chunks.json`；要自动从后端同步 Chunks 需按真实业务需要增加索引同步任务。

真实 LLM 模式：`AGENT_MODE=llm` + `OPENAI_API_BASE`、`OPENAI_API_KEY`、`OPENAI_MODEL`；要求 Provider 支持 Chat Completions 的 function `tool_calls`。无需向公开仓库提交 `.env`。

## 系统结构

```text
Finance-RAG-Agent-Complete/
  finance_agent/
    api.py            FastAPI 入口
    graph.py          LangGraph StateGraph / Checkpointer
    router.py         离线意图路由
    llm.py            可选 LLM Tool Calling + 答案生成
    store.py          模拟产品 / FinDataHub API Client
    retrieval.py      FAISS / 相似检索 / 元数据过滤
    ingest.py         PDF 文本抽取与分块
    settings.py       环境配置
    factory.py        初始化 Agent
  scripts/
    demo.py           多轮对话演示
    evaluate.py       工作流 Smoke Test
    ingest_pdf.py     PDF 转 Chunk JSON
    check_package.py 无第三方依赖结构检查
  data/
    products.json     3 个模拟金融产品
    chunks.json       6 条模拟产品说明资料
    eval_cases.jsonl  5 条路由评测示例
  tests/              单元 / LangGraph / API 测试
  docs/               Windows 启动、架构、API、面试介绍
  pyproject.toml / requirements.txt
  Dockerfile / docker-compose.yml
```

## 作品真实性与安全

本项目为公开教学型原型，数据全部为合成示例，未使用企业仓库、公司业务数据或凭证。**没有开展真实金融产品推荐、交易和生产环境部署**。`InMemorySaver` 仅适用于本地演示；本 API 未配置用户鉴权，请仅绑定本机。投递简历时应基于自己真实完成的复现、改动、测试填入成果，不应把示例脚本当作已经完成的企业项目。

参阅 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 与 [`docs/INTERVIEW_WALKTHROUGH.md`](docs/INTERVIEW_WALKTHROUGH.md)。
