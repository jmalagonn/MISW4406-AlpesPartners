import os, json, logging, sys
from infrastructure.pulsar.consumer import start_consumer
from infrastructure.db.db import session_scope
from application.commands.create_affiliate import CreateAffiliate, handle_create_affiliate
from application.commands.rename_affiliate import RenameAffiliate, handle_rename_affiliate

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s"
)

TOPIC_COMMANDS_AFFILIATES = os.getenv("TOPIC_COMMANDS_AFFILIATES")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")

def handle(payload, props):
    logging.info("Received msg props=%s payload=%s", props, json.dumps(payload))
    
    command_name = props.get("name")
    
    if command_name == "CreateAffiliate":
        try:    
            with session_scope() as session:      
                cmd = CreateAffiliate(**payload)
                new_id = handle_create_affiliate(cmd, session)
                
                logging.info("Affiliate created id=%s", new_id)
        except Exception as e:
            logging.exception("handle_create_affiliate failed: %s", e)
            raise
    
    elif command_name == "RenameAffiliate":
        try:    
            with session_scope() as session:      
                cmd = RenameAffiliate(**payload)
                handle_rename_affiliate(cmd, session)
                
                logging.info("Affiliate renamed id=%s", cmd.id)
        except Exception as e:
            logging.exception("handle_rename_affiliate failed: %s", e)
            raise
      

def main():
    start_consumer(TOPIC_COMMANDS_AFFILIATES, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
    main()
