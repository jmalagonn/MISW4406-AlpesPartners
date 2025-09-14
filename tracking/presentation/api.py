from flask import Blueprint, request, jsonify
from sqlalchemy import text
import uuid
from infrastructure.db.projections import get_daily_stats
from infrastructure.db.db import session_scope
from application.handlers.interaction_handler import InteractionHandler
from application.queries.query_handlers import InteractionQueryHandler


bp = Blueprint("tracking", __name__, url_prefix="/tracking")

@bp.get("/health")
def health():
    return {"status": "Tracking health serivce ok"}, 200

@bp.get("/stats/daily")
def stats_daily():
    return {"items": get_daily_stats()}, 200


@bp.post("/interactions")
def track_interaction():
    """
    Endpoint para trackear interacciones
    """
    try:
        data = request.get_json()
        
        handler = InteractionHandler()
        interaction_id = handler.handle_track_interaction(data)
        
        return {
            "status": "success",
            "interaction_id": interaction_id
        }, 201
        
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": "Internal server error"}, 500

# ===== READ ENDPOINTS (CQRS Read Side) =====

@bp.get("/interactions")
def get_interactions():
    """
    Endpoint para obtener todas las interacciones (Read Side)
    """
    try:
        with session_scope() as session:
            query_handler = InteractionQueryHandler(session)
            interactions = query_handler.get_all_interactions()
            
            return {
                "status": "success",
                "data": [
                    {
                        "id": str(interaction.id),
                        "interaction_type": interaction.interaction_type,
                        "target_element_id": interaction.target_element_id,
                        "target_element_type": interaction.target_element_type,
                        "campaign_id": interaction.campaign_id,
                        "timestamp": interaction.timestamp.isoformat(),
                        "created_at": interaction.created_at.isoformat(),
                        "updated_on": interaction.updated_on.isoformat()
                    }
                    for interaction in interactions
                ]
            }, 200
            
    except Exception as e:
        return {"error": "Internal server error"}, 500

@bp.get("/interactions/<interaction_id>")
def get_interaction_by_id(interaction_id):
    """
    Endpoint para obtener una interacción específica por ID (Read Side)
    """
    try:
        with session_scope() as session:
            query_handler = InteractionQueryHandler(session)
            
            interaction = query_handler.get_interaction_by_id(uuid.UUID(interaction_id))
            
            if not interaction:
                return {"error": "Interaction not found"}, 404
            
            return {
                "status": "success",
                "data": {
                    "id": str(interaction.id),
                    "interaction_type": interaction.interaction_type,
                    "target_element_id": interaction.target_element_id,
                    "target_element_type": interaction.target_element_type,
                    "campaign_id": interaction.campaign_id,
                    "timestamp": interaction.timestamp.isoformat(),
                    "created_at": interaction.created_at.isoformat(),
                    "updated_on": interaction.updated_on.isoformat()
                }
            }, 200
            
    except ValueError as e:
        return {"error": "Invalid interaction ID"}, 400
    except Exception as e:
        return {"error": "Internal server error"}, 500