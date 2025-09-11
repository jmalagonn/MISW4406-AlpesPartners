from flask import Blueprint, current_app, request, jsonify
from .http import make_client, forward_headers

bp = Blueprint("api", __name__)

@bp.post("/afiliate")
def create_affiliate():

    timeout = current_app.config["DEFAULT_TIMEOUT"]
    affiliates_url = current_app.config["AFFILIATES_SVC_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
      # Pending implementation: call affiliates service to create an affiliate
      ...

    return jsonify({}), 202
