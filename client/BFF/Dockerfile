# ---------- builder ----------
FROM python:3.12-slim AS builder
ENV PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && pip wheel --no-deps --wheel-dir /wheels -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# ---------- runtime ----------
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN useradd -m appuser
WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install /wheels/*

COPY . .

USER appuser
EXPOSE 8080

ENV WEB_CONCURRENCY=2 THREADS=4 TIMEOUT=30
CMD ["sh", "-c", "exec gunicorn \
  --bind=0.0.0.0:8080 \
  --workers=${WEB_CONCURRENCY:-2} \
  --threads=${THREADS:-4} \
  --timeout=${TIMEOUT:-30} \
  --access-logfile - --error-logfile - \
  --log-level info --capture-output \
  wsgi:app"]
