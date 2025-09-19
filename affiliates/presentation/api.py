from flask import Blueprint, jsonify
from affiliates.infrastructure.db.db import session_scope
from affiliates.application.queries.query_handlers import handle_list_affiliates

bp = Blueprint("affiliates", __name__, url_prefix="/affiliates")

@bp.get("/health")
def health():
    return {"status": "Affiliates health serivce ok"}, 200

@bp.get("/")
def list_affiliates():
    with session_scope() as s:
        data = handle_list_affiliates(s)
        
    return jsonify(data), 200
