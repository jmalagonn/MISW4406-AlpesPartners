import os, pulsar, uuid
from datetime import datetime
from time import timezone


def now_iso():
    return datetime.now(timezone.utc).isoformat()
  

def new_envelope(msg_type: str, saga_id: str | None, payload: dict, headers: dict | None = None):
    return {
        "msg_id": str(uuid.uuid4()),
        "saga_id": saga_id,
        "causation_id": None,
        "correlation_id": saga_id,
        "type": msg_type,
        "occurred_at": now_iso(),
        "payload": payload,
        "headers": {"schema_version": "1", **(headers or {})}
    }
    

PULSAR_URL = os.getenv("PULSAR_URL")
def client() -> pulsar.Client:
  return pulsar.Client(PULSAR_URL)