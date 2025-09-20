import logging, os, json
from alliances.infrastructure.db.db import SessionLocal
from alliances.infrastructure.db.db_models import SagaInstance
from seedwork.infrastructure.pulsar.publisher import publish
from seedwork.infrastructure.pulsar.pulsar_client import new_envelope


TOPIC_COMMANDS_AFFILIATES = os.getenv("TOPIC_COMMANDS_AFFILIATES", "commands.affiliates")

def handle_interactions_info_built_event(payload, props):
    """Handle InteractionsInfoBuilt event from tracking service"""
    try:
        saga_id = payload.get("saga_id")
        interactions_data = payload.get("payload", {})
        
        logging.info("Processing InteractionsInfoBuilt event for saga_id: %s", saga_id)
        
        # Extract interaction data
        interactions = interactions_data.get("interactions", [])
        post_id = interactions_data.get("post_id")
        total_interactions = interactions_data.get("total_interactions", 0)
        
        logging.info("Found %d interactions for post_id: %s", total_interactions, post_id)
        
        # Update SAGA instance with commission data
        with SessionLocal.begin() as session:
            saga_instance = session.get(SagaInstance, saga_id)
            if not saga_instance:
                logging.error("SAGA instance not found: %s", saga_id)
                return
            
            # Update SAGA data with commission information
            saga_data = dict(saga_instance.data) if saga_instance.data else {}
            saga_data.update({
                "interactions_data": interactions_data,
                "total_interactions": total_interactions,
                "post_id": post_id
            })
            
            saga_instance.data = saga_data
            saga_instance.step = 1  # Move to next step
            session.commit()
            
            logging.info("Updated SAGA %s with total interacions: %f", saga_id, total_interactions)
            
            # Publish next command in the SAGA
            publish_next_saga_command(session, saga_instance)
            
    except Exception as e:
        logging.error("Error processing InteractionsInfoBuilt event: %s", str(e))
        # Handle SAGA failure
        handle_saga_failure(saga_id, str(e))


def publish_next_saga_command(session, saga_instance):
    """Publish the next command in the SAGA sequence"""
    try:
        saga_data = dict(saga_instance.data) if saga_instance.data else {}
        post_id = saga_data.get("post_id")
        
        # Extract interactions data from SAGA
        interactions_data = saga_data.get("interactions_data", {})
        total_interactions = interactions_data.get("total_interactions", 0)
        
        # Create cost calculation command
        calculate_cost_command = {
            "saga_id": saga_instance.saga_id,
            "post_id": post_id,
            "interactions_count": total_interactions,
            "interactions_data": interactions_data
        }
        
        envelope = new_envelope(
            command_type="command.CalculateCost",
            saga_id=str(saga_instance.saga_id),
            payload=calculate_cost_command,
            properties={"name": "CalculateCost"}
        )
        
        # Publish to payment processing topic
        publish(
            topic=TOPIC_COMMANDS_AFFILIATES,
            key=str(saga_instance.saga_id),
            payload=envelope.payload,
            properties=envelope.properties
        )
        
        logging.info("Published ProcessPayment command for SAGA: %s", saga_instance.saga_id)
        
    except Exception as e:
        logging.error("Error publishing next SAGA command: %s", str(e))
        raise


def handle_saga_failure(saga_id, error_message):
    """Handle SAGA failure by updating status"""
    try:
        with SessionLocal.begin() as session:
            from alliances.infrastructure.db.db_models import SagaStatus
            
            saga_instance = session.get(SagaInstance, saga_id)
            if saga_instance:
                saga_instance.status = SagaStatus.FAILED
                saga_data = dict(saga_instance.data) if saga_instance.data else {}
                saga_data["error"] = error_message
                saga_instance.data = saga_data
                session.commit()
                
                logging.error("SAGA %s marked as failed: %s", saga_id, error_message)
                
    except Exception as e:
        logging.error("Error handling SAGA failure: %s", str(e))


def handle_cost_calculated_event(payload, props):
    """Handle CostCalculated event from affiliates service"""
    try:
        saga_id = payload.get("saga_id")
        cost_data = payload.get("payload", {})
        
        logging.info("Processing CostCalculated event for saga_id: %s", saga_id)
        
        # Extract cost data
        post_id = cost_data.get("post_id")
        total_cost = cost_data.get("total_cost", 0)
        base_cost = cost_data.get("base_cost", 0)
        engagement_multiplier = cost_data.get("engagement_multiplier", 1.0)
        interactions_count = cost_data.get("interactions_count", 0)
        
        logging.info("Cost calculated for post_id %s: total_cost=%f", post_id, total_cost)
        
        # Update SAGA instance with cost data
        with SessionLocal.begin() as session:
            from alliances.infrastructure.db.db_models import SagaStatus
            
            saga_instance = session.get(SagaInstance, saga_id)
            if not saga_instance:
                logging.error("SAGA instance not found: %s", saga_id)
                return
            
            # Update SAGA data with cost information
            saga_data = dict(saga_instance.data) if saga_instance.data else {}
            saga_data.update({
                "cost_data": cost_data,
                "total_cost": total_cost,
                "base_cost": base_cost,
                "engagement_multiplier": engagement_multiplier,
                "interactions_count": interactions_count,
                "post_id": post_id
            })
            
            saga_instance.data = saga_data
            saga_instance.step = 2  # Move to next step
            saga_instance.status = SagaStatus.COMPLETED  # Mark as completed
            session.commit()
            
            logging.info("Updated SAGA %s with cost data: %f", saga_id, total_cost)
            
            # Persist cost information to post_costs table
            persist_post_cost(session, saga_data, cost_data)
            
            # Log SAGA completion
            logging.info("SAGA %s COMPLETED successfully. Step: %d, Status: %s", 
                        saga_id, saga_instance.step, saga_instance.status)
            
            # Publish SAGA completion event
            publish_saga_completion_event(saga_id, saga_data, cost_data)
            
            # Verify SAGA completion
            verify_saga_completion(saga_id)
            
    except Exception as e:
        logging.error("Error processing CostCalculated event: %s", str(e))
        # Handle SAGA failure
        handle_saga_failure(saga_id, str(e))


def persist_post_cost(session, saga_data, cost_data):
    """Persist cost information to post_costs table"""
    try:
        from alliances.infrastructure.db.db_models import PostCostsDBModel
        import uuid
        
        # Extract required data
        post_id = cost_data.get("post_id")
        total_cost = cost_data.get("total_cost", 0)
        brand_id = saga_data.get("brand_id")
        affiliate_id = saga_data.get("affiliate_id")
        
        if not post_id:
            logging.error("Cannot persist post cost: post_id is missing")
            return
            
        if not brand_id:
            logging.error("Cannot persist post cost: brand_id is missing")
            return
            
        if not affiliate_id:
            logging.error("Cannot persist post cost: affiliate_id is missing")
            return
          
        # Create PostCostsDBModel instance
        post_cost = PostCostsDBModel(
            id=uuid.uuid4(),
            post_id=uuid.UUID(post_id),
            affiliate_id=uuid.UUID(affiliate_id),
            brand_id=uuid.UUID(brand_id),
            cost=total_cost
        )
        
        # Add to session and commit
        session.add(post_cost)
        session.commit()
        
        logging.info("Successfully persisted post cost: post_id=%s, cost=%f, brand_id=%s, affiliate_id=%s", 
                    post_id, total_cost, brand_id, affiliate_id)
        
    except Exception as e:
        logging.error("Error persisting post cost: %s", str(e))
        session.rollback()
        raise e


def publish_saga_completion_event(saga_id, saga_data, cost_data):
    """Publish SAGA completion event to notify other services"""
    try:
        from seedwork.infrastructure.pulsar.pulsar_client import new_envelope
        
        # Get the events topic for alliances
        topic = os.getenv("TOPIC_EVENTS_ALLIANCES", "events.alliances")
        
        # Create completion event payload
        completion_payload = {
            "saga_id": saga_id,
            "saga_type": "CommissionPayout",
            "status": "COMPLETED",
            "step": 2,
            "total_cost": cost_data.get("total_cost", 0),
            "post_id": cost_data.get("post_id"),
            "brand_id": saga_data.get("brand_id"),
            "affiliate_id": saga_data.get("affiliate_id"),
            "completed_at": cost_data.get("calculated_at")
        }
        
        # Create event envelope
        envelope = new_envelope(
            command_type="event.SagaCompleted",
            saga_id=str(saga_id),
            payload=completion_payload,
            properties={"name": "SagaCompleted"}
        )
        
        # Publish completion event
        publish(
            topic=topic,
            key=str(saga_id),
            payload=envelope.payload,
            properties=envelope.properties
        )
        
        logging.info("Published SAGA completion event for saga_id: %s", saga_id)
        
    except Exception as e:
        logging.error("Error publishing SAGA completion event: %s", str(e))
        # Don't raise here as the SAGA is already completed


def verify_saga_completion(saga_id):
    """Verify that a SAGA is properly completed"""
    try:
        with SessionLocal.begin() as session:
            from alliances.infrastructure.db.db_models import SagaStatus
            
            saga_instance = session.get(SagaInstance, saga_id)
            if not saga_instance:
                logging.error("SAGA instance not found: %s", saga_id)
                return False
                
            # Check if SAGA is completed
            is_completed = (
                saga_instance.status == SagaStatus.COMPLETED and
                saga_instance.step == 2 and
                saga_instance.data is not None
            )
            
            if is_completed:
                logging.info("SAGA %s verification: COMPLETED ✓", saga_id)
                logging.info("  - Status: %s", saga_instance.status)
                logging.info("  - Step: %d", saga_instance.step)
                logging.info("  - Has data: %s", saga_instance.data is not None)
            else:
                logging.warning("SAGA %s verification: NOT COMPLETED ✗", saga_id)
                logging.warning("  - Status: %s (expected: %s)", saga_instance.status, SagaStatus.COMPLETED)
                logging.warning("  - Step: %d (expected: 2)", saga_instance.step)
                logging.warning("  - Has data: %s", saga_instance.data is not None)
                
            return is_completed
            
    except Exception as e:
        logging.error("Error verifying SAGA completion: %s", str(e))
        return False
    
    