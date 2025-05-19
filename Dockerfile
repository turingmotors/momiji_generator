# Dockerfile 修正版
FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv
WORKDIR /app

COPY pyproject.toml ./

COPY src ./src
COPY retrieve_text_from_jsonl.py .

RUN uv pip install . --system --no-cache-dir \
  && rm -rf /root/.cache

ENTRYPOINT ["python", "/app/retrieve_text_from_jsonl.py"]
CMD []
