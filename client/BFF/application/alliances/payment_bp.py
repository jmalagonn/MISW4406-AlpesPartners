import json, uuid
from flask import jsonify, request, current_app
from application.routes import bp
from infrastructure.pulsar_ext import pulsar_ext

@bp.post("/create-payment-order")
def create_payment_order():
    body = request.get_json(force=True)
    current_app.logger.info(f"Paymend order creation requested with params: {json.dumps(body)}") 
    
    cmd_id = str(uuid.uuid4())
    corr_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    topic = current_app.config["TOPIC_COMMANDS_ALLIANCES"]
    
    producer = pulsar_ext.producer(topic)
    producer.send(
        json.dumps(body).encode("utf-8"),
        partition_key=cmd_id,
        properties={
            "commanType": "create.payment.order",
            "commandId": cmd_id,
            "correlationId": corr_id,
            "name": "CreatePaymentOrder"
        },
    )   
    
    return jsonify({"status": "accepted", "trackingId": cmd_id}), 202