import os, json, logging, sys, time
from infrastructure.pulsar.consumer import start_consumer
from infrastructure.db.projections import ensure_projection, increment_status
from application.handlers.interaction_handler import InteractionHandler
from application.commands.build_interactions_info import BuildInteractionsInfo, BuildInteractionsInfoHandler
from infrastructure.db.db import session_scope

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
  
  elif command_name == "BuildInteractionsInfo":
    handle_build_interactions_info_command(payload, props)
  
  else:
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


def handle_build_interactions_info_command(payload, props):
    """
    Maneja el comando BuildInteractionsInfo desde Pulsar
    """
    try:
        logging.info("Processing BuildInteractionsInfo command with payload: %s", json.dumps(payload))
        
        # Extract command data from payload
        start_date = payload.get("start_date")
        end_date = payload.get("end_date") 
        post_id = payload.get("post_id")
        saga_id = payload.get("saga_id")
        
        # Validate required fields
        if not post_id:
            raise ValueError("post_id is required for BuildInteractionsInfo command")
        
        # Create command object
        command = BuildInteractionsInfo(
            start_date=start_date,
            end_date=end_date,
            post_id=post_id
        )
        
        # Create environment context for the handler
        env = {
            "saga_id": saga_id,
            "command_id": props.get("commandId"),
            "correlation_id": props.get("correlationId")
        }
        
        # Execute command within database session
        with session_scope() as session:
            handler = BuildInteractionsInfoHandler(session, env)
            handler.handle(command)
            session.commit()  # Ensure changes are committed
        
        logging.info("BuildInteractionsInfo command processed successfully for post_id: %s", post_id)
        increment_status(status="ok")
        
    except Exception as e:
        logging.error("Error processing BuildInteractionsInfo command: %s", str(e))
        increment_status(status="error")

def main():
  ensure_projection()  # crea tabla de proyección si no existe
  start_consumer(TOPIC_COMMANDS_TRACKING, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
  main()