import os, json, logging, sys
from affiliates.application.commands.create_post import CreatePost, CreatePostHandler
from affiliates.infrastructure.db.db import session_scope
from affiliates.application.commands.create_affiliate import CreateAffiliate, CreateAffiliateHandler
from affiliates.application.commands.calculate_cost import CalculateCost, CalculateCostHandler
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
        
    elif command_name == "CreatePost":
        try:    
            with session_scope() as session:      
                cmd = CreatePost(**payload)
                
                handler = CreatePostHandler(session)        
                handler.handle(cmd)
                
                logging.info("Post created successfully")
        except Exception as e:
            logging.exception("handle_create_post failed: %s", e)
            raise
            
    elif command_name == "CalculateCost":
        handle_calculate_cost_command(payload, props)
        
    else:
        logging.warning("Unknown command: %s", command_name)


def handle_calculate_cost_command(payload, props):
    """Handle CalculateCost command for SAGA"""
    try:
        logging.info("Processing CalculateCost command with payload: %s", json.dumps(payload))
        
        # Extract command data from payload
        post_id = payload.get("post_id")
        saga_id = payload.get("saga_id")
        interactions_count = payload.get("interactions_count", 0)
        interactions_data = payload.get("interactions_data", {})
        
        # Validate required fields
        if not post_id:
            raise ValueError("post_id is required for CalculateCost command")
        if not saga_id:
            raise ValueError("saga_id is required for CalculateCost command")
        
        # Create command object
        command = CalculateCost(
            post_id=post_id,
            saga_id=saga_id,
            interactions_count=interactions_count,
            interactions_data=interactions_data
        )
        
        # Create environment context for the handler
        env = {
            "saga_id": saga_id,
            "command_id": props.get("commandId"),
            "correlation_id": props.get("correlationId")
        }
        
        # Execute command within database session
        with session_scope() as session:
            handler = CalculateCostHandler(session, env)
            handler.handle(command)
        
        logging.info("CalculateCost command processed successfully for post_id: %s", post_id)
        
    except Exception as e:
        logging.error("Error processing CalculateCost command: %s", str(e))
        raise


def main():
    start_consumer(TOPIC_COMMANDS_AFFILIATES, SUBSCRIPTION_NAME, handle)


if __name__ == "__main__":
    main()
