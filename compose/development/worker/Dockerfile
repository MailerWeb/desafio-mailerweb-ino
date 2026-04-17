FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend/pyproject.toml .
RUN uv pip install --system -e ".[dev]"

COPY backend/ .

CMD ["celery", "-A", "app.worker.celery_app", "worker", "--loglevel=info"]
