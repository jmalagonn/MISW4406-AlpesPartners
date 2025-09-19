FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./alliances/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY seedwork/ ./seedwork/
COPY alliances/ ./alliances/

ENV PYTHONPATH=/app

EXPOSE 8020

CMD ["gunicorn", "-b", "0.0.0.0:8020", "alliances.wsgi:app"]