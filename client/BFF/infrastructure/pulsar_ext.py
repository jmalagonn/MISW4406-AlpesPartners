# Minimal extension to manage a single client and lazy producers
import os, atexit, time, pulsar
from pulsar import Client

def _with_retry(thunk, what, tries=30, base=0.5, cap=8.0):
    delay = base
    for i in range(tries):
        try:
            return thunk()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 1.7, cap)

class PulsarExt:
    def __init__(self):
        self._client: Client | None = None
        self._producers: dict[str, pulsar.Producer] = {}
        self._url: str | None = None
        

    def init_app(self, app):
        self._url = app.config.get("PULSAR_URL")
        self._client = pulsar.Client(self._url)
        
        atexit.register(self.close)
        
        
    def _client_or_connect(self):
        if not self._client:
            self._client = _with_retry(
                lambda: pulsar.Client(self._url, operation_timeout_seconds=5, connection_timeout_ms=3000),
                "pulsar client connect"
            )
        return self._client
                

    def producer(self, topic: str) -> pulsar.Producer:
        if not self._client:
            raise RuntimeError("Pulsar client not initialized yet")
        if topic not in self._producers:
            self._producers[topic] = _with_retry(
                lambda: self._client_or_connect().create_producer(
                    topic,
                    batching_enabled=True,
                    batching_max_publish_delay_ms=5,
                    block_if_queue_full=True,
                ),
                f"create_producer({topic})"
            )
        return self._producers[topic]
    
    
    def close(self):
        for p in self._producers.values():
            try: p.flush(); p.close()
            except Exception: pass
        self._producers.clear()
        if self._client:
            try: self._client.close()
            except Exception: pass
            self._client = None

pulsar_ext = PulsarExt()
