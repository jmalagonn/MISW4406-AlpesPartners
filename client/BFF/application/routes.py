import json
import uuid
from flask import Blueprint, Response, current_app, request, jsonify
import requests
from infrastructure.pulsar_ext import pulsar_ext
from infrastructure.bff_http import make_client, forward_headers

_HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "content-length"
}

bp = Blueprint("api", __name__)

@bp.before_app_request
def _log_request():
    req_id = request.headers.get("X-Request-ID", "-")
    current_app.logger.info("REQ %s %s req_id=%s", request.method, request.path, req_id)
    
## Health checks
    
@bp.get("/affiliates/health")
def affiliates_health_check():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    affiliates_url = current_app.config["AFFILIATES_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{affiliates_url}/affiliates/health", headers=headers) 

    return _proxy_response(response)


@bp.get("/loyalty/health")
def loyalty_health_check():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    loyalty_url = current_app.config["LOYALTY_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{loyalty_url}/loyalty/health", headers=headers) 

    return _proxy_response(response)


@bp.post("/brand")
def create_affiliate():
    current_app.logger.info(f"Brand creation requested") 

    body = request.get_json(force=True)
    cmd_id = str(uuid.uuid4())
    corr_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    topic = current_app.config["TOPIC_COMMANDS_ALLIANCES"]
    
    producer = pulsar_ext.producer(topic)    
    producer.send(
        json.dumps(body).encode("utf-8"),
        partition_key=cmd_id,
        properties={
            "commandId": cmd_id,
            "correlationId": corr_id,
            "name": "CreateBrand"
        },
    )
    
    return jsonify({"status": "accepted", "trackingId": cmd_id}), 202
  
def _proxy_response(upstream: requests.Response) -> Response:
    out = Response(upstream.content, status=upstream.status_code)
    
    for k, v in upstream.headers.items():
        if k.lower() not in _HOP_BY_HOP:
            out.headers[k] = v
    return out  
