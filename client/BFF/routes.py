from flask import Blueprint, current_app, request, jsonify
from bff_http import make_client, forward_headers

bp = Blueprint("api", __name__)

@bp.before_app_request
def _log_request():
    req_id = request.headers.get("X-Request-ID", "-")
    current_app.logger.info("REQ %s %s req_id=%s", request.method, request.path, req_id)

@bp.post("/affiliate")
def create_affiliate():
    current_app.logger.info(f"Affiliate creation requested") 

    timeout = current_app.config["DEFAULT_TIMEOUT"]
    affiliates_url = current_app.config["AFFILIATES_SVC_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        body = request.get_json(force=True) or {}
    #   client.post(f"{affiliates_url}/affiliates", json=body, headers=headers)
    #   current_app.logger.info(f"Affiliate creation requested, req_id={req_id}")     

    return jsonify({}), 202
