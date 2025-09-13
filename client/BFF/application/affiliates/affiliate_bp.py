import uuid, json
from urllib.parse import urljoin
from flask import request, jsonify, current_app, Response
from application.routes import bp
from infrastructure.bff_http import make_client
from infrastructure.pulsar_ext import pulsar_ext


@bp.post("/affiliate")
def create_affiliate():
    current_app.logger.info(f"Affiliate creation requested") 

    body = request.get_json(force=True)
    cmd_id = str(uuid.uuid4())
    corr_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    topic = current_app.config["TOPIC_COMMANDS_AFFILIATES"]
    
    producer = pulsar_ext.producer(topic)    
    producer.send(
        json.dumps(body).encode("utf-8"),
        partition_key=cmd_id,
        properties={
            "commandId": cmd_id,
            "correlationId": corr_id,
            "name": "CreateAffiliate",
        },
    )
    
    return jsonify({"status": "accepted", "trackingId": cmd_id}), 202
  

@bp.get("/affiliates")
def get_affiliates():
    service_url = current_app.config.get("AFFILIATES_API_URL")
    
    if not service_url:
        return {"error": "misconfig", "detail": "AFFILIATES_API_URL is missing"}, 500
    
    api_path = "affiliates/"
    final_url = urljoin(service_url.rstrip('/') + '/', api_path.lstrip('/'))
    
    current_app.logger.info(f"Forwarding to {final_url}")    
    with make_client(current_app.config["API_TIMEOUT"]) as client:
        response = client.get(final_url, params=request.args, headers=request.headers)
    
    return Response(response.content, status=response.status_code, headers=dict(response.headers))