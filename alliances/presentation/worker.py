import os, json, logging, sys
from threading import Event, Thread
from seedwork.infrastructure.pulsar.consumer import start_consumer
from alliances.infrastructure.db.db import session_scope
from alliances.application.commands.create_brand import CreateBrand, CreateBrandHandler
from alliances.sagas.create_payment_order_handler import (
    handle_interactions_info_built_event,
    handle_cost_calculated_event
)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s"
)
LOG = logging.getLogger("alliances-main")

TOPIC_COMMANDS_ALLIANCES = os.getenv("TOPIC_COMMANDS_ALLIANCES")
TOPIC_EVENTS_TRACKING = os.getenv("TOPIC_EVENTS_TRACKING")
TOPIC_EVENTS_AFFILIATES = os.getenv("TOPIC_EVENTS_AFFILIATES")
SUBSCRIPTION_NAME = os.getenv("SUB-ALLIANCES-SVC", "alliances-svc")
SUB_SAGA_TRACKING = os.getenv("SUB_SAGA_TRACKING", "saga-tracking")
SUB_SAGA_AFFILIATES = os.getenv("SUB_SAGA_AFFILIATES", "saga-affiliates")

STOP = Event()


def handle_alliances_commands(payload, props):
  logging.info("Received msg props=%s payload=%s", props, json.dumps(payload))
    
  command_name = props.get("name")
  
  if command_name == "CreateBrand":
    try:    
      with session_scope() as session:      
        cmd = CreateBrand(**payload)
        
        handler = CreateBrandHandler(session)        
        handler.handle(cmd)
        
        logging.info("Brand created successfully")
    except Exception as e:
        logging.exception("handle_create_brand failed: %s", e)
        raise
    
  else:
        logging.warning("Unknown command: %s", command_name)
        

def handle_tracking_events(payload, props):
    """Handle events from tracking service for SAGA coordination"""
    logging.info("Received tracking event props=%s payload=%s", props, json.dumps(payload))
    
    event_type = props.get("name")
    saga_id = payload.get("saga_id")
    
    if not saga_id:
        logging.warning("Received tracking event without saga_id, ignoring")
        return
    
    if event_type == "InteractionsInfoBuilt":
        handle_interactions_info_built_event(payload, props)
    else:
        logging.info("Unhandled tracking event type: %s", event_type)
        
        
def handle_affiliate_events(payload, props):
    """Handle events from affiliates service for SAGA coordination"""
    logging.info("Received affiliate event props=%s payload=%s", props, json.dumps(payload))
    
    event_type = props.get("name")
    saga_id = payload.get("saga_id")
    
    if not saga_id:
        logging.warning("Received affiliate event without saga_id, ignoring")
        return
    
    if event_type == "CostCalculated":
        handle_cost_calculated_event(payload, props)
    else:
        logging.info("Unhandled affiliate event type: %s", event_type)



def _run_consumer(topic, sub, handler):
    LOG.info("Starting consumer topic=%s subscription=%s", topic, sub)
    start_consumer(topic, sub, handler)
      

def main():
  def _sig(*_):
        LOG.info("Stop signal received; shutting down consumers…")
        STOP.set()
        
  threads = [
        Thread(target=_run_consumer, args=(TOPIC_COMMANDS_ALLIANCES, SUBSCRIPTION_NAME, handle_alliances_commands), daemon=True),
        Thread(target=_run_consumer, args=(TOPIC_EVENTS_TRACKING, SUB_SAGA_TRACKING,  handle_tracking_events), daemon=True),
        Thread(target=_run_consumer, args=(TOPIC_EVENTS_AFFILIATES, SUB_SAGA_AFFILIATES, handle_affiliate_events), daemon=True)
    ]
        
  for thread in threads:
        thread.start()
        
  try:
        for thread in threads:
            thread.join()
  except KeyboardInterrupt:
        LOG.info("Shutting down...")
        STOP.set()


if __name__ == "__main__":
  main()