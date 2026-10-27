# Windows PowerShell 零基础启动

1. 从 GitHub 或 ZIP 解压项目，确保进入包含 `pyproject.toml` 的工程根目录。
2. 安装 Python 3.11（64位）。打开 VS Code 终端（PowerShell）。

```powershell
cd Finance-RAG-Agent-Complete
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m scripts.demo
python -m pytest -q
python -m uvicorn finance_agent.api:app --reload --port 8010
```

3. 访问 `http://127.0.0.1:8010/docs`，执行 `/api/v1/ask`：

```json
{"thread_id":"demo","question":"DEMO001的风险等级是什么？"}
```

再用相同 `thread_id` 发送：

```json
{"thread_id":"demo","question":"它的赎回规则是什么？"}
```

4. 如果激活虚拟环境受到策略限制，用 `.\.venv\Scripts\python.exe` 代替所有 `python` 命令，不必修改全局 PowerShell 策略。
5. 安装依赖需要网络。`faiss-cpu` 或 `langgraph` 安装失败时，请核对 Python 3.11、64 位及当前网络镜像；不要直接双击 `.py` 运行。
6. 如果 ZIP 下载不完整，重新保存到本地后使用资源管理器 **全部解压缩**，不要双击直接在压缩包内启动。
