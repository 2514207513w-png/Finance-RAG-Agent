FROM python:3.11-slim
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir -e .
EXPOSE 8010
CMD ["uvicorn", "finance_agent.api:app", "--host", "0.0.0.0", "--port", "8010"]
