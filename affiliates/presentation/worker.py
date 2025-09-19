import os, json, logging, sys
from affiliates.application.commands.create_post import CreatePost, CreatePostHandler
from affiliates.infrastructure.db.db import session_scope
from affiliates.application.commands.create_affiliate import CreateAffiliate, CreateAffiliateHandler
from seedwork.infrastructure.pulsar.consumer import start_consumer

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
                
                handler = CreateAffiliateHandler(session)        
                handler.handle(cmd)
                
                logging.info("Affiliate created successfully")
        except Exception as e:
            logging.exception("handle_create_affiliate failed: %s", e)
            raise
        
    if command_name == "CreatePost":
        try:    
            with session_scope() as session:      
                cmd = CreatePost(**payload)
                
                handler = CreatePostHandler(session)        
                handler.handle(cmd)
                
                logging.info("Post created successfully")
        except Exception as e:
            logging.exception("handle_create_post failed: %s", e)
            raise
      

def main():
    start_consumer(TOPIC_COMMANDS_AFFILIATES, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
    main()
