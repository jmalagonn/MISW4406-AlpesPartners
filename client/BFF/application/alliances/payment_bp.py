import json, uuid
from flask import jsonify, request, current_app
from application.routes import bp
from infrastructure.pulsar_ext import pulsar_ext
from infrastructure.bff_http import make_client, forward_headers

@bp.post("/create-payment-order")
def create_payment_order():
    body = request.get_json(force=True)
    current_app.logger.info(f"Payment order creation requested with params: {json.dumps(body)}") 
    
    # Forward headers and get correlation ID
    headers, corr_id = forward_headers(request.headers)
    
    # Get alliances API URL from config
    alliances_api_url = current_app.config.get("ALLIANCES_API_URL", "http://alliances:8020")
    
    try:
        # Make HTTP request to alliances service to start SAGA
        with make_client(timeout_seconds=30.0) as client:
            response = client.post(
                f"{alliances_api_url}/alliances/create-payment-order",
                json=body,
                headers=headers
            )
            
            if response.status_code == 202:
                saga_data = response.json()
                current_app.logger.info(f"SAGA started successfully: {saga_data}")
                
                return jsonify({
                    "status": "accepted", 
                    "saga_id": saga_data.get("saga_id"),
                    "trackingId": saga_data.get("saga_id"),
                    "message": "Payment order SAGA started successfully"
                }), 202
            else:
                current_app.logger.error(f"Failed to start SAGA: {response.status_code} - {response.text}")
                return jsonify({
                    "status": "error",
                    "message": f"Failed to start payment order SAGA: {response.text}"
                }), response.status_code
                
    except Exception as e:
        current_app.logger.error(f"Error calling alliances service: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error starting payment order SAGA: {str(e)}"
        }), 500


@bp.get("/saga-status/<saga_id>")
def get_saga_status(saga_id):
    """Get the status of a SAGA instance"""
    current_app.logger.info(f"SAGA status requested for: {saga_id}")
    
    # Forward headers and get correlation ID
    headers, corr_id = forward_headers(request.headers)
    
    # Get alliances API URL from config
    alliances_api_url = current_app.config.get("ALLIANCES_API_URL", "http://alliances:8020")
    
    try:
        # Make HTTP request to alliances service to get SAGA status
        with make_client(timeout_seconds=30.0) as client:
            response = client.get(
                f"{alliances_api_url}/alliances/sagas/{saga_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                saga_data = response.json()
                current_app.logger.info(f"SAGA status retrieved: {saga_data}")
                return jsonify(saga_data), 200
            elif response.status_code == 404:
                return jsonify({
                    "status": "error",
                    "message": "SAGA instance not found"
                }), 404
            else:
                current_app.logger.error(f"Failed to get SAGA status: {response.status_code} - {response.text}")
                return jsonify({
                    "status": "error",
                    "message": f"Failed to get SAGA status: {response.text}"
                }), response.status_code
                
    except Exception as e:
        current_app.logger.error(f"Error calling alliances service: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error getting SAGA status: {str(e)}"
        }), 500


@bp.get("/post-costs")
def get_post_costs():
    """Get all post costs from alliances service"""
    current_app.logger.info("Post costs query requested")
    
    # Forward headers and get correlation ID
    headers, corr_id = forward_headers(request.headers)
    
    # Get alliances API URL from config
    alliances_api_url = current_app.config.get("ALLIANCES_API_URL", "http://alliances:8020")
    
    try:
        # Make HTTP request to alliances service to get post costs
        with make_client(timeout_seconds=30.0) as client:
            response = client.get(
                f"{alliances_api_url}/alliances/post-costs",
                headers=headers
            )
            
            if response.status_code == 200:
                post_costs_data = response.json()
                current_app.logger.info(f"Post costs retrieved successfully: {len(post_costs_data.get('data', []))} records")
                return jsonify(post_costs_data), 200
            else:
                current_app.logger.error(f"Failed to get post costs: {response.status_code} - {response.text}")
                return jsonify({
                    "status": "error",
                    "message": f"Failed to get post costs: {response.text}"
                }), response.status_code
                
    except Exception as e:
        current_app.logger.error(f"Error calling alliances service: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error getting post costs: {str(e)}"
        }), 500