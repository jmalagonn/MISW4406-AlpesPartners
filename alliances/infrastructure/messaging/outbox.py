from datetime import datetime
from time import timezone
from infrastructure.db.db_models import Outbox
from seedwork.infrastructure.pulsar.pulsar_client import new_envelope
from sqlalchemy.orm import Session


def enqueue_command(session: Session, topic: str, msg_type: str, saga_id: str | None, payload: dict, headers=None):
    env = new_envelope(msg_type, saga_id, payload, headers)
    ob = Outbox(topic=topic, payload=env, headers=env.get("headers", {}))
    session.add(ob)
    return env


def mark_published(session: Session, outbox_id, published_at=None):
    ob = session.get(Outbox, outbox_id)
    if ob and not ob.published_at:
        ob.published_at = published_at or datetime.now(timezone.utc)
        session.add(ob)