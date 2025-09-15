import os
from flask import Blueprint, Response, current_app, request, jsonify
import requests
from infrastructure.pulsar_ext import pulsar_ext
from infrastructure.bff_http import make_client, forward_headers

TOPIC_COMMANDS_TRACKING = os.getenv("TOPIC_COMMANDS_TRACKING")

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

@bp.post("/track")
def track_client():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "invalid_json"}), 400

    client_id = payload.get("clientId")
    if not client_id:
        return jsonify({"error": "clientId required"}), 400

    event = {
        "eventType": "ClientTracked",
        "clientId": client_id,
        "campaignId": payload.get("campaignId", "default"),
        "metadata": payload.get("metadata", {}),
        "timestamp": payload.get("timestamp") or __import__("datetime").datetime.utcnow().isoformat()
    }

    def on_publish_done(exc):
        if exc:
            current_app.logger.exception(
                "Failed to publish tracking event for client=%s campaign=%s", client_id, event["campaignId"]
            )
        else:
            current_app.logger.info(
                "PUBLISHED tracking event for client=%s campaign=%s", client_id, event["campaignId"]
            )

    try:
        pulsar_ext.publish_event(TOPIC_COMMANDS_TRACKING, event, callback=on_publish_done)
    except Exception as exc:
        current_app.logger.exception("Failed to queue tracking event")
        return jsonify({"error": "publish_failed", "detail": str(exc)}), 500

    return jsonify({"status": "accepted", "event": event}), 202

from .alliances import brand_bp
from .affiliates import affiliate_bp
  
def _proxy_response(upstream: requests.Response) -> Response:
    out = Response(upstream.content, status=upstream.status_code)
    
    for k, v in upstream.headers.items():
        if k.lower() not in _HOP_BY_HOP:
            out.headers[k] = v
    return out  
