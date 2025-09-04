from celery.utils.log import get_task_logger
from infrastructure.celery_app import celery
from infrastructure.db import session_scope
from application.commands import CreateAfiliate, RenameAfiliate
from application.command_handlers import (
    handle_create_afiliate, handle_rename_afiliate
)

log = get_task_logger(__name__)

@celery.task(name="commands.create_afiliate", autoretry_for=(Exception,), retry_backoff=5, max_retries=3)
def create_customer_task(payload: dict) -> dict:
    with session_scope() as session:
        cmd = CreateAfiliate(**payload)
        new_id = handle_create_afiliate(cmd, session)
        log.info("Customer created id=%s", new_id)
        return {"id": new_id}

@celery.task(name="commands.rename_afiliate", autoretry_for=(Exception,), retry_backoff=5, max_retries=3)
def rename_customerafiliate_task(payload: dict) -> dict:
    with session_scope() as session:
        cmd = RenameAfiliate(**payload)
        handle_rename_afiliate(cmd, session)
        return {"ok": True}
