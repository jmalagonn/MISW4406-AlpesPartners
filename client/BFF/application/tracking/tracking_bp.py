from flask import current_app, request
from application.routes import bp, proxy_response
from infrastructure.bff_http import forward_headers, make_client


@bp.get("/tracking/health")
def tracking_health_check():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{tracking_url}/tracking/health", headers=headers) 

    return proxy_response(response)


@bp.get("/tracking/interactions")
def get_tracking_interactions():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{tracking_url}/tracking/interactions", headers=headers) 

    return proxy_response(response)


@bp.get("/tracking/stats/daily")
def get_tracking_daily_stats():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.get(f"{tracking_url}/tracking/stats/daily", headers=headers) 

    return proxy_response(response)


@bp.post("/tracking/interactions")
def create_tracking_interaction():
    timeout = current_app.config["DEFAULT_TIMEOUT"]
    tracking_url = current_app.config["TRACKING_API_URL"]

    headers, req_id = forward_headers(request.headers)

    with make_client(timeout) as client:
        response = client.post(f"{tracking_url}/tracking/interactions", 
                              json=request.get_json(), 
                              headers=headers) 

    return proxy_response(response)