from flask import Blueprint, jsonify, request
from alliances.application.queries.list_brands import ListBrands, handle_list_brands
from alliances.infrastructure.db.db import session_scope


bp = Blueprint("alliances", __name__, url_prefix="/alliances")

@bp.get("/health")
def health():
    return {"status": "Alliances health serivce ok"}, 200

@bp.get("/brands")
def list_brands():
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    
    with session_scope() as session:
        data = handle_list_brands(ListBrands(limit=limit, offset=offset), session)
        
    return jsonify(data), 200