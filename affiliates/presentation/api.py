from flask import Blueprint, request, jsonify
from infrastructure.db.db import session_scope
from application.queries.queries import GetAffiliateById, ListAffiliates
from application.queries.query_handlers import handle_get_affiliate_by_id, handle_list_affiliates

bp = Blueprint("affiliates", __name__, url_prefix="/affiliates")

@bp.get("/health")
def health():
    return {"status": "Affiliates health serivce ok"}, 200

@bp.get("/")
def list_affiliates():
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    with session_scope() as s:
        data = handle_list_affiliates(ListAffiliates(limit=limit, offset=offset), s)
    return jsonify(data), 200

@bp.get("/<affiliate_id>")
def get_affiliate(affiliate_id: str):
    with session_scope() as s:
        data = handle_get_affiliate_by_id(GetAffiliateById(affiliate_id=affiliate_id), s)
    if not data:
        return {"error": "not found"}, 404
    return jsonify(data), 200
