import requests
from flask import Blueprint, Response, current_app, request
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


def proxy_response(upstream: requests.Response) -> Response:
    out = Response(upstream.content, status=upstream.status_code)
    
    for k, v in upstream.headers.items():
        if k.lower() not in _HOP_BY_HOP:
            out.headers[k] = v
    return out  

from .alliances import brand_bp, payment_bp
from .affiliates import affiliate_bp, posts_bp
from .tracking import tracking_bp
  

