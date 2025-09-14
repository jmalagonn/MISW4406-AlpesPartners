import json
from .pulsar_client import client
from .props import with_correlation

def publish(topic: str, key: str, payload: dict, properties: dict):
  prod = client().create_producer(topic, batching_enabled=True)
  prod.send(
    json.dumps(payload, default=str).encode("utf-8"),
    partition_key=key,
    # properties={k: str(v) for k, v in (properties or {}).items()},
    properties={k: str(v) for k, v in with_correlation(properties).items()},
  )