from datetime import datetime
from flask import Blueprint, request, jsonify
from infrastructure.db.db import session_scope
from application.queries.queries import GetAffiliateById, ListAffiliates
from application.queries.query_handlers import handle_get_affiliate_by_id, handle_list_affiliates
from infrastructure.celery_app import celery

bp = Blueprint("affiliates", __name__, url_prefix="/affiliates")

@bp.get("/health")
def health():
    return {"status": "ok"}, 200

# ===== QUERIES (read) =====
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

# ===== COMMANDS (write) =====
@bp.post("/")
def create_affiliate():
    body = request.get_json(force=True)
    required = {"name"}
    if not body or not required.issubset(body):
        return {"error": "name is required"}, 400

    task = celery.send_task("commands.create_affiliate", args=[{"name": body["name"], "created_at": datetime.now().isoformat()}])
    
    return {
        "status": "accepted",
        "message": "Affiliate creation enqueued",
        "tracking_task_id": task.id,
        "how_to_read": "GET /affiliates?limit=50 or GET /affiliates/<id> when you have it"
    }, 202

@bp.post("/<affiliate_id>/rename")
def rename(affiliate_id: str):
    body = request.get_json(force=True) or {}
    name = body.get("name")
    if not name:
        return {"error": "name is required"}, 400
    celery.send_task("commands.rename_affiliate", args=[{"affiliate_id": affiliate_id, "name": name}])
    return {"status": "accepted"}, 202
