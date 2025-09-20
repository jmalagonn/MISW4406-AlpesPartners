import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from flask import current_app, jsonify
from infrastructure.repository import InteractionRepository
from infrastructure.pulsar.publisher import publish
from config import settings

def _now_iso(): 
  return datetime.now(timezone.utc).isoformat()


def mk_evt(msg_type: str, saga_id: str, payload: dict, msg_id: str | None = None, headers: dict | None = None):
    return {
        "msg_id": msg_id or str(uuid.uuid4()),
        "saga_id": saga_id,
        "correlation_id": saga_id,
        "type": msg_type,
        "occurred_at": _now_iso(),
        "payload": payload,
        "headers": {"schema_version": "1", **(headers or {})},
    }


@dataclass
class BuildInteractionsInfo:
    start_date: str
    end_date: str
    post_id: str
    
    
class BuildInteractionsInfoHandler:
    def __init__(self, session, env):
        self.session = session
        self.env = env
        
    def handle(self, command: BuildInteractionsInfo):
        from flask import current_app
        import logging
        
        logger = logging.getLogger(__name__)
        logger.info(f"Processing BuildInteractionsInfo for post_id: {command.post_id}")
        
        repo = InteractionRepository(self.session)
        interactions_by_post = repo.get_interations_by_post_id(
          post_id=command.post_id,
          start_date=command.start_date,
          end_date=command.end_date
        )
        
        logger.info(f"Found {len(interactions_by_post)} interactions for post_id: {command.post_id}")
        
        saga_id = self.env.get("saga_id")
        topic = settings.TOPIC_EVENTS_TRACKING
        
        # Convert interactions to serializable format
        interactions_data = []
        for interaction in interactions_by_post:
            interactions_data.append({
                "id": str(interaction.id),
                "interaction_type": interaction.interaction_type.value,
                "target_element_id": interaction.target_element.element_id,
                "target_element_type": interaction.target_element.element_type,
                "campaign_id": interaction.campaign_id.value,
                "timestamp": interaction.timestamp.isoformat(),
                "created_at": interaction.created_at.isoformat(),
                "updated_on": interaction.updated_on.isoformat()
            })
        
        evt = mk_evt(
          "event.interactionsInfoBuilt",
          saga_id,
          {
              "interactions": interactions_data,
              "post_id": command.post_id,
              "start_date": command.start_date,
              "end_date": command.end_date,
              "total_interactions": len(interactions_data)
          }
        )
        
        try:
          logger.info(f"Publishing InteractionsInfoBuilt event for saga_id: {saga_id}")
          publish(topic=topic, key=saga_id, payload=evt, properties={"name": "InteractionsInfoBuilt"})
          logger.info(f"Successfully published InteractionsInfoBuilt event for saga_id: {saga_id}")
        except Exception as e:
          logger.error(f"Failed to publish InteractionsInfoBuilt event: {str(e)}")
          raise e
    
    
    

    

