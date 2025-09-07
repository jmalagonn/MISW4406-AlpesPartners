from celery.utils.log import get_task_logger
from infrastructure.celery_app import celery
from infrastructure.db.db import session_scope
from application.commands.commands import CreateAffiliate, RenameAffiliate
from application.commands.command_handlers import (
    handle_create_affiliate, handle_rename_affiliate
)

log = get_task_logger(__name__)

@celery.task(name="commands.create_affiliate", autoretry_for=(Exception,), retry_backoff=5, max_retries=3)
def create_affiliate_task(payload: dict) -> dict:
    with session_scope() as session:
        cmd = CreateAffiliate(**payload)
        new_id = handle_create_affiliate(cmd, session)
        log.info("Customer created id=%s", new_id)
        return {"id": new_id}

@celery.task(name="commands.rename_affiliate", autoretry_for=(Exception,), retry_backoff=5, max_retries=3)
def rename_affiliate_task(payload: dict) -> dict:
    with session_scope() as session:
        cmd = RenameAffiliate(**payload)
        handle_rename_affiliate(cmd, session)
        return {"ok": True}
    
@celery.task(name="events.affiliate_created")
def publish_affiliate_created_event(event_data):
    
    log.info("Publishing event: %s", event_data)
    return {"published": True}
