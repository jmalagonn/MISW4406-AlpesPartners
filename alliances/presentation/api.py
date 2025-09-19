from flask import Blueprint, jsonify
from alliances.application.queries.list_brands import handle_list_brands
from alliances.infrastructure.db.db import session_scope


bp = Blueprint("alliances", __name__, url_prefix="/alliances")

@bp.get("/health")
def health():
    return {"status": "Alliances health serivce ok"}, 200

@bp.get("/brands")
def list_brands():    
    with session_scope() as session:
        data = handle_list_brands(session)
        
    return jsonify(data), 200