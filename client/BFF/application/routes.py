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


@bp.get("/tracking/health")
def tracking_health_check():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{tracking_url}/tracking/health", headers=headers) 

    return _proxy_response(response)


@bp.get("/tracking/interactions")
def get_tracking_interactions():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{tracking_url}/tracking/interactions", headers=headers) 

    return _proxy_response(response)


@bp.get("/tracking/stats/daily")
def get_tracking_daily_stats():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{tracking_url}/tracking/stats/daily", headers=headers) 

    return _proxy_response(response)


@bp.post("/tracking/interactions")
def create_tracking_interaction():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.post(f"{tracking_url}/tracking/interactions", 
                              json=request.get_json(), 
                              headers=headers) 

    return _proxy_response(response)

from .alliances import brand_bp
from .affiliates import affiliate_bp
  
def _proxy_response(upstream: requests.Response) -> Response:
    out = Response(upstream.content, status=upstream.status_code)
    
    for k, v in upstream.headers.items():
        if k.lower() not in _HOP_BY_HOP:
            out.headers[k] = v
    return out  
