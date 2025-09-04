import os
from celery import Celery
from config import settings

celery = Celery(
    settings.SERVICE_NAME,
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery.conf.task_routes = {
    "commands.*": {"queue": "commands"},
}
