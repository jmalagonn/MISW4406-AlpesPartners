import os, json, logging
import sys
from infrastructure.pulsar.consumer import start_consumer
from application.commands.command_handlers import handle_create_brand

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
    handle_create_brand(payload)


def main():
  start_consumer(TOPIC_COMMANDS_ALLIANCES, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
  main()