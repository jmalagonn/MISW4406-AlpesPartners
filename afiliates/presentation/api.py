from flask import Blueprint, request, jsonify
from infrastructure.db import session_scope
from application.queries import GetAfiliateById, ListAfiliates
from application.query_handlers import handle_get_afiliate_by_id, handle_list_afiliates
from infrastructure.celery_app import celery

bp = Blueprint("afiliates", __name__, url_prefix="/afiliates")

@bp.get("/health")
def health():
    return {"status": "ok"}, 200

# ===== QUERIES (read) =====
@bp.get("/")
def list_afiliates():
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    with session_scope() as s:
        data = handle_list_afiliates(ListAfiliates(limit=limit, offset=offset), s)
    return jsonify(data), 200

@bp.get("/<afiliate_id>")
def get_afiliate(afiliate_id: str):
    with session_scope() as s:
        data = handle_get_afiliate_by_id(GetAfiliateById(afiliate_id=afiliate_id), s)
    if not data:
        return {"error": "not found"}, 404
    return jsonify(data), 200

# ===== COMMANDS (write) =====
@bp.post("/")
def create_afiliate():
    body = request.get_json(force=True)
    required = {"name"}
    if not body or not required.issubset(body):
        return {"error": "name is required"}, 400

    # Fire-and-forget command; worker will do the write
    task = celery.send_task("commands.create_afiliate", args=[{"name": body["name"]}])
    
    # We don’t wait for result (CQS). Tell the client how to read later.
    return {
        "status": "accepted",
        "message": "Afiliate creation enqueued",
        "tracking_task_id": task.id,
        "how_to_read": "GET /afiliates?limit=50 or GET /afiliates/<id> when you have it"
    }, 202

@bp.post("/<afiliate_id>/rename")
def rename(afiliate_id: str):
    body = request.get_json(force=True) or {}
    name = body.get("name")
    if not name:
        return {"error": "name is required"}, 400
    celery.send_task("commands.rename_afiliate", args=[{"afiliate_id": afiliate_id, "name": name}])
    return {"status": "accepted"}, 202
