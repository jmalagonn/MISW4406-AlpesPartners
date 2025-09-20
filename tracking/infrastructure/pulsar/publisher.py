import json
from .pulsar_client import client
from .props import with_correlation

import json, pulsar, time, atexit
from .pulsar_client import client

_producers: dict[str, pulsar.Producer] = {}

def _get_producer(topic: str) -> pulsar.Producer:
    if topic not in _producers:
        _producers[topic] = client().create_producer(
            topic,
            batching_enabled=True,
            batching_max_messages=500,
            batching_max_publish_delay_ms=5,
            compression_type=pulsar.CompressionType.LZ4,
            send_timeout_millis=30000,
        )
    return _producers[topic]

def publish(topic: str, key: str, payload: dict, properties: dict | None = None,
            tries: int = 5, base_delay: float = 0.2, cap: float = 2.0):
    prod = _get_producer(topic)
    body = json.dumps(payload, default=str).encode("utf-8")
    props = {k: str(v) for k, v in (properties or {}).items()}
    delay = base_delay
    for i in range(tries):
        try:
            prod.send(body, partition_key=key, properties=props)
            return
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 2, cap)
            
def _close_all():
    for p in _producers.values():
        try: p.close()
        except: pass

atexit.register(_close_all)