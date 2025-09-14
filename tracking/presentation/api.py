from flask import Blueprint
from sqlalchemy import text
from infrastructure.db.projections import get_daily_stats


bp = Blueprint("tracking", __name__, url_prefix="/tracking")

@bp.get("/health")
def health():
    return {"status": "Tracking health serivce ok"}, 200

@bp.get("/stats/daily")
def stats_daily():
    return {"items": get_daily_stats()}, 200