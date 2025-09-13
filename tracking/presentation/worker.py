import os, json, logging, sys
from infrastructure.pulsar.consumer import start_consumer

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s"
)

TOPIC_COMMANDS_TRACKING = os.getenv("TOPIC_COMMANDS_TRACKING")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")


def handle(payload, props):
  logging.info("Received msg props=%s payload=%s", props, json.dumps(payload))
      

def main():
  start_consumer(TOPIC_COMMANDS_TRACKING, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
  main()