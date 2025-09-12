# Minimal extension to manage a single client and lazy producers
import os, atexit, pulsar
from pulsar import Client

class PulsarExt:
    def __init__(self):
        self._client: Client | None = None
        self._producers: dict[str, pulsar.Producer] = {}
        self._url: str | None = None
        

    def init_app(self, app):
        self._url = app.config.get("PULSAR_URL")
        self._client = pulsar.Client(self._url)
        
        atexit.register(self.close)
                

    def producer(self, topic: str) -> pulsar.Producer:
        if not self._client:
            raise RuntimeError("Pulsar client not initialized yet")
        if topic not in self._producers:
            self._producers[topic] = self._client.create_producer(
                topic,
                batching_enabled=True,
                batching_max_publish_delay_ms=5,
                block_if_queue_full=True,
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
