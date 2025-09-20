import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from seedwork.infrastructure.pulsar.publisher import publish
from seedwork.infrastructure.pulsar.pulsar_client import new_envelope


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
class CalculateCost:
    post_id: str
    saga_id: str
    interactions_count: int = 0
    interactions_data: dict = None


class CalculateCostHandler:
    def __init__(self, session, env):
        self.session = session
        self.env = env
        
    def handle(self, command: CalculateCost):
        import logging
        from flask import current_app
        from affiliates.infrastructure.db.db_models import PostDBModel

        logger = logging.getLogger(__name__)
        logger.info(f"Processing CalculateCost for post_id: {command.post_id}")

        # Fetch post details to get brand_id and affiliate_id
        post = self.session.get(PostDBModel, command.post_id)
        if not post:
            logger.error(f"Post not found: {command.post_id}")
            raise ValueError(f"Post not found: {command.post_id}")
        
        brand_id = str(post.brand_id)
        affiliate_id = str(post.affiliate_id)
        
        logger.info(f"Found post details: brand_id={brand_id}, affiliate_id={affiliate_id}")

        # Calculate cost based on post and interactions
        base_cost = 1.0  # Base cost per post
        interaction_cost = 0.05  # Cost per interaction
        engagement_multiplier = 1.0  # Base engagement multiplier

        # Calculate interaction-based costs
        interactions_count = command.interactions_count or 0
        interaction_total_cost = interactions_count * interaction_cost

        # Calculate engagement multiplier based on interactions
        if interactions_count > 0:
            if interactions_count >= 100:
                engagement_multiplier = 2.0  # High engagement
            elif interactions_count >= 50:
                engagement_multiplier = 1.5  # Medium engagement
            elif interactions_count >= 10:
                engagement_multiplier = 1.2  # Low engagement

        # Calculate total cost
        base_total = base_cost + interaction_total_cost
        total_cost = base_total * engagement_multiplier

        logger.info(f"Calculated cost for post_id: {command.post_id}")
        logger.info(f"  - Base cost: {base_cost}")
        logger.info(f"  - Interactions: {interactions_count}")
        logger.info(f"  - Interaction cost: {interaction_total_cost}")
        logger.info(f"  - Engagement multiplier: {engagement_multiplier}")
        logger.info(f"  - Total cost: {total_cost}")

        saga_id = command.saga_id
        topic = current_app.config.get("TOPIC_EVENTS_AFFILIATES", "events.affiliates")

        # Create cost calculation event
        cost_data = {
            "post_id": command.post_id,
            "brand_id": brand_id,
            "affiliate_id": affiliate_id,
            "base_cost": base_cost,
            "interactions_count": interactions_count,
            "interaction_cost": interaction_cost,
            "interaction_total_cost": interaction_total_cost,
            "engagement_multiplier": engagement_multiplier,
            "total_cost": total_cost,
            "calculated_at": _now_iso()
        }
        
        evt = mk_evt(
            "event.CostCalculated",
            saga_id,
            cost_data
        )
        
        try:
            logger.info(f"Publishing CostCalculated event for saga_id: {saga_id}")
            publish(
                topic=topic, 
                key=saga_id, 
                payload=evt, 
                properties={"name": "CostCalculated"}
            )
            logger.info(f"Successfully published CostCalculated event for saga_id: {saga_id}")
        except Exception as e:
            logger.error(f"Failed to publish CostCalculated event: {str(e)}")
            raise e
