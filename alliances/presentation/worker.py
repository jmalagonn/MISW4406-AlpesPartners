import os, json, logging, sys
from seedwork.infrastructure.pulsar.consumer import start_consumer
from alliances.infrastructure.db.db import session_scope
from alliances.application.commands.create_brand import CreateBrand, CreateBrandHandler

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s"
)

TOPIC_COMMANDS_ALLIANCES = os.getenv("TOPIC_COMMANDS_ALLIANCES")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")


def handle(payload, props):
  logging.info("Received msg props=%s payload=%s", props, json.dumps(payload))
    
  if props.get("name") == "CreateBrand":
    try:    
      with session_scope() as session:      
        cmd = CreateBrand(**payload)
        
        handler = CreateBrandHandler(session)        
        handler.handle(cmd)
        
        logging.info("Brand created successfully")
    except Exception as e:
        logging.exception("handle_create_brand failed: %s", e)
        raise
      

def main():
  start_consumer(TOPIC_COMMANDS_ALLIANCES, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
  main()