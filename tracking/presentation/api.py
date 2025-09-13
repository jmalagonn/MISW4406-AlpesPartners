from flask import Blueprint
from infrastructure.db.db import session_scope


bp = Blueprint("tracking", __name__, url_prefix="/tracking")

@bp.get("/health")
def health():
    return {"status": "Tracking health serivce ok"}, 200