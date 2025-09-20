from uuid import uuid4
from flask import Blueprint, current_app, jsonify, request
from alliances.application.queries.list_brands import handle_list_brands
from alliances.infrastructure.db.db import session_scope
from alliances.infrastructure.db.db_models import SagaInstance
from seedwork.infrastructure.pulsar.publisher import publish
from seedwork.infrastructure.pulsar.pulsar_client import new_envelope


bp = Blueprint("alliances", __name__, url_prefix="/alliances")

@bp.get("/health")
def health():
    return {"status": "Alliances health serivce ok"}, 200

@bp.get("/brands")
def list_brands():    
    with session_scope() as session:
        data = handle_list_brands(session)
        
    return jsonify(data), 200

@bp.post("/create-payment-order")
def close_payout():
    body = request.get_json()
    saga_id = uuid4()
    
    with session_scope() as s:
        s.add(SagaInstance(
            saga_id=saga_id, saga_type="CommissionPayout",
            status="RUNNING", step=0,
            data={"brand_id": body["brand_id"], "affiliate_id": body["affiliate_id"], "period": body["period"]}
        ))
        
        topic = current_app.config["TOPIC_COMMANDS_TRACKING"]
        env = new_envelope("command.BuildInteractionsInfo", saga_id, body)
        
        publish(
            topic,
            key=str(saga_id),
            payload=env,
            properties={"name": "BuildInteractionsInfo"}
        )
    
    return {"saga_id": str(saga_id)}, 202
