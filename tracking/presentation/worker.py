import os, json, logging, sys
import os, json, logging, sys, time
from infrastructure.pulsar.consumer import start_consumer
from infrastructure.db.projections import ensure_projection, increment_status

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s"
)

TOPIC_COMMANDS_TRACKING = os.getenv("TOPIC_COMMANDS_TRACKING")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")
BENCHMARK_MODE = os.getenv("BENCHMARK_MODE", "false").lower() == "true"


def handle(payload, props):
  
  logging.info("Received msg props=%s payload=%s", props, json.dumps(payload))

  # Modo bench: para realizar prueba de capacidad
  if BENCHMARK_MODE:
    ts_ms = int(time.time() * 1000)
    logging.info("CAPACITY BENCH processed_ms=%d", ts_ms)
    return

  increment_status(status="ok")

def main():
  ensure_projection()  # crea tabla de proyección si no existe
  start_consumer(TOPIC_COMMANDS_TRACKING, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
  main()