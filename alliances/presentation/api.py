from uuid import uuid4, UUID
from flask import Blueprint, current_app, jsonify, request
from datetime import datetime
from alliances.application.queries.list_brands import handle_list_brands
from alliances.application.queries.get_post_costs import (
    handle_get_post_costs,
    handle_get_post_cost_by_id,
    handle_get_post_costs_by_post_id,
    handle_get_post_costs_by_affiliate_id,
    handle_get_post_costs_by_brand_id,
    handle_get_post_costs_summary,
    handle_get_total_cost_by_affiliate,
    handle_get_total_cost_by_brand,
    handle_get_total_cost_by_post
)
from alliances.application.dto.post_costs_dto import PostCostFiltersDTO
from alliances.infrastructure.db.db import session_scope
from alliances.infrastructure.db.db_models import SagaInstance
from alliances.config import settings
from seedwork.infrastructure.pulsar.publisher import publish
from seedwork.infrastructure.pulsar.pulsar_client import new_envelope


bp = Blueprint("alliances", __name__, url_prefix="/alliances")

@bp.get("/health")
def health():
    return {"status": "Alliances health serivce ok"}, 200

@bp.get("/brands")
def list_brands():    
    with session_scope() as session:
        data = handle_list_brands(session)
        
    return jsonify(data), 200

@bp.post("/create-payment-order")
def close_payout():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"error": "Request body is required"}), 400
            
        # Validate required fields
        required_fields = ["post_id", "start_date", "end_date"]
        for field in required_fields:
            if field not in body:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        saga_id = uuid4()
        
        with session_scope() as s:
            s.add(SagaInstance(
                saga_id=saga_id, 
                saga_type="CommissionPayout",
                status="RUNNING", step=0,
                data={
                    "post_id": body["post_id"], 
                    "start_date": body["start_date"], 
                    "end_date": body["end_date"]
                }
            ))
            
            topic = settings.TOPIC_COMMANDS_TRACKING
            env = new_envelope("command.BuildInteractionsInfo", str(saga_id), body)
            
            publish(
                topic,
                key=str(saga_id),
                payload=env,
                properties={"name": "BuildInteractionsInfo"}
            )
        
        return {"saga_id": str(saga_id)}, 202
        
    except Exception as e:
        current_app.logger.error(f"Error creating payment order: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# Post Costs API Endpoints

@bp.get("/post-costs")
def get_post_costs():
    """Get post costs with optional filters and pagination"""
    try:
        # Parse query parameters
        filters = PostCostFiltersDTO.from_request_args(request.args)
        
        # Convert string UUIDs to UUID objects
        try:
            if filters.post_id:
                filters.post_id = UUID(filters.post_id)
            if filters.affiliate_id:
                filters.affiliate_id = UUID(filters.affiliate_id)
            if filters.brand_id:
                filters.brand_id = UUID(filters.brand_id)
        except ValueError as e:
            return jsonify({"error": f"Invalid UUID format: {str(e)}"}), 400
        
        # Parse date strings
        try:
            if filters.start_date:
                filters.start_date = datetime.fromisoformat(filters.start_date.replace('Z', '+00:00'))
            if filters.end_date:
                filters.end_date = datetime.fromisoformat(filters.end_date.replace('Z', '+00:00'))
        except ValueError as e:
            return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
        
        with session_scope() as session:
            result = handle_get_post_costs(session, filters)
            
        return jsonify(result.to_dict()), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid parameter: {str(e)}"}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting post costs: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/<uuid:cost_id>")
def get_post_cost_by_id(cost_id):
    """Get a specific post cost by ID"""
    try:
        with session_scope() as session:
            result = handle_get_post_cost_by_id(session, cost_id)
            
        if result:
            return jsonify(result.to_dict()), 200
        else:
            return jsonify({"error": "Post cost not found"}), 404
            
    except Exception as e:
        current_app.logger.error(f"Error getting post cost by ID: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/post/<uuid:post_id>")
def get_post_costs_by_post_id(post_id):
    """Get all post costs for a specific post"""
    try:
        with session_scope() as session:
            results = handle_get_post_costs_by_post_id(session, post_id)
            
        return jsonify([result.to_dict() for result in results]), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting post costs by post ID: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/affiliate/<uuid:affiliate_id>")
def get_post_costs_by_affiliate_id(affiliate_id):
    """Get all post costs for a specific affiliate"""
    try:
        with session_scope() as session:
            results = handle_get_post_costs_by_affiliate_id(session, affiliate_id)
            
        return jsonify([result.to_dict() for result in results]), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting post costs by affiliate ID: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/brand/<uuid:brand_id>")
def get_post_costs_by_brand_id(brand_id):
    """Get all post costs for a specific brand"""
    try:
        with session_scope() as session:
            results = handle_get_post_costs_by_brand_id(session, brand_id)
            
        return jsonify([result.to_dict() for result in results]), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting post costs by brand ID: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/summary")
def get_post_costs_summary():
    """Get post costs summary with statistics"""
    try:
        # Parse query parameters
        filters = PostCostFiltersDTO.from_request_args(request.args)
        
        # Convert string UUIDs to UUID objects
        try:
            if filters.post_id:
                filters.post_id = UUID(filters.post_id)
            if filters.affiliate_id:
                filters.affiliate_id = UUID(filters.affiliate_id)
            if filters.brand_id:
                filters.brand_id = UUID(filters.brand_id)
        except ValueError as e:
            return jsonify({"error": f"Invalid UUID format: {str(e)}"}), 400
        
        # Parse date strings
        try:
            if filters.start_date:
                filters.start_date = datetime.fromisoformat(filters.start_date.replace('Z', '+00:00'))
            if filters.end_date:
                filters.end_date = datetime.fromisoformat(filters.end_date.replace('Z', '+00:00'))
        except ValueError as e:
            return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
        
        with session_scope() as session:
            result = handle_get_post_costs_summary(session, filters)
            
        return jsonify(result.to_dict()), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid parameter: {str(e)}"}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting post costs summary: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/affiliate/<uuid:affiliate_id>/total")
def get_total_cost_by_affiliate(affiliate_id):
    """Get total cost for a specific affiliate"""
    try:
        with session_scope() as session:
            total_cost = handle_get_total_cost_by_affiliate(session, affiliate_id)
            
        return jsonify({"affiliate_id": str(affiliate_id), "total_cost": total_cost}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting total cost by affiliate: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/brand/<uuid:brand_id>/total")
def get_total_cost_by_brand(brand_id):
    """Get total cost for a specific brand"""
    try:
        with session_scope() as session:
            total_cost = handle_get_total_cost_by_brand(session, brand_id)
            
        return jsonify({"brand_id": str(brand_id), "total_cost": total_cost}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting total cost by brand: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.get("/post-costs/post/<uuid:post_id>/total")
def get_total_cost_by_post(post_id):
    """Get total cost for a specific post"""
    try:
        with session_scope() as session:
            total_cost = handle_get_total_cost_by_post(session, post_id)
            
        return jsonify({"post_id": str(post_id), "total_cost": total_cost}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting total cost by post: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
