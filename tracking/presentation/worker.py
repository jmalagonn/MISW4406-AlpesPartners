import os, json, logging, sys, time
from infrastructure.pulsar.consumer import start_consumer
from infrastructure.db.projections import ensure_projection, increment_status
from application.handlers.interaction_handler import InteractionHandler

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

  command_name = props.get("name", "")
  
  if command_name == "TrackInteraction":
    handle_track_interaction_command(payload, props)
  else:
    # Comportamiento por defecto para otros comandos
    increment_status(status="ok")


def handle_track_interaction_command(payload, props):
    """
    Maneja el comando TrackInteraction desde Pulsar
    """
    try:
        
        handler = InteractionHandler()
        interaction_id = handler.handle_track_interaction(payload)
        
        logging.info("Interaction tracked successfully: %s", interaction_id)
        
        increment_status(status="ok")
        
    except Exception as e:
        logging.error("Error processing TrackInteraction command: %s", str(e))
        increment_status(status="error")

def main():
  ensure_projection()  # crea tabla de proyección si no existe
  start_consumer(TOPIC_COMMANDS_TRACKING, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
  main()