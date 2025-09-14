from flask import Blueprint, request, jsonify
from sqlalchemy import text
from infrastructure.db.projections import get_daily_stats
from application.handlers.interaction_handler import InteractionHandler


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