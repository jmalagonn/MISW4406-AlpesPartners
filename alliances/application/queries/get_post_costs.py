from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from alliances.infrastructure.repository.post_costs_repository import PostCostsRepositoryDB
from alliances.application.dto.post_costs_dto import (
    PostCostDTO, 
    PostCostSummaryDTO, 
    PostCostFiltersDTO, 
    PostCostResponseDTO
)


@dataclass
class GetPostCosts:
    """Query to get post costs with optional filters"""
    post_id: Optional[UUID] = None
    affiliate_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    min_cost: Optional[float] = None
    max_cost: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    order_by: str = "created_at"
    order_direction: str = "desc"
    limit: Optional[int] = None
    offset: Optional[int] = None


def handle_get_post_costs(session: Session, filters: PostCostFiltersDTO) -> PostCostResponseDTO:
    """Handle get post costs query with filters and pagination"""
    repo = PostCostsRepositoryDB(session)
    
    # Get filtered post costs
    post_costs = repo.get_with_filters(
        post_id=filters.post_id,
        affiliate_id=filters.affiliate_id,
        brand_id=filters.brand_id,
        min_cost=filters.min_cost,
        max_cost=filters.max_cost,
        start_date=filters.start_date,
        end_date=filters.end_date,
        order_by=filters.order_by,
        order_direction=filters.order_direction,
        limit=filters.limit,
        offset=filters.offset
    )
    
    # Get total count for pagination
    total_count = repo.count_by_filters(
        post_id=filters.post_id,
        affiliate_id=filters.affiliate_id,
        brand_id=filters.brand_id,
        min_cost=filters.min_cost,
        max_cost=filters.max_cost,
        start_date=filters.start_date,
        end_date=filters.end_date
    )
    
    # Convert to DTOs
    cost_dtos = [PostCostDTO.from_db_model(cost) for cost in post_costs]
    
    # Calculate pagination info
    page_size = filters.limit or total_count
    page = (filters.offset or 0) // page_size + 1 if page_size > 0 else 1
    total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 1
    
    return PostCostResponseDTO(
        data=cost_dtos,
        total_count=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


def handle_get_post_cost_by_id(session: Session, cost_id: UUID) -> Optional[PostCostDTO]:
    """Handle get post cost by ID query"""
    repo = PostCostsRepositoryDB(session)
    post_cost = repo.get_by_id(cost_id)
    
    if post_cost:
        return PostCostDTO.from_db_model(post_cost)
    return None


def handle_get_post_costs_by_post_id(session: Session, post_id: UUID) -> List[PostCostDTO]:
    """Handle get post costs by post ID query"""
    repo = PostCostsRepositoryDB(session)
    post_costs = repo.get_by_post_id(post_id)
    
    return [PostCostDTO.from_db_model(cost) for cost in post_costs]


def handle_get_post_costs_by_affiliate_id(session: Session, affiliate_id: UUID) -> List[PostCostDTO]:
    """Handle get post costs by affiliate ID query"""
    repo = PostCostsRepositoryDB(session)
    post_costs = repo.get_by_affiliate_id(affiliate_id)
    
    return [PostCostDTO.from_db_model(cost) for cost in post_costs]


def handle_get_post_costs_by_brand_id(session: Session, brand_id: UUID) -> List[PostCostDTO]:
    """Handle get post costs by brand ID query"""
    repo = PostCostsRepositoryDB(session)
    post_costs = repo.get_by_brand_id(brand_id)
    
    return [PostCostDTO.from_db_model(cost) for cost in post_costs]


def handle_get_post_costs_summary(session: Session, filters: PostCostFiltersDTO) -> PostCostSummaryDTO:
    """Handle get post costs summary query"""
    repo = PostCostsRepositoryDB(session)
    
    # Get all post costs with filters (no pagination for summary)
    post_costs = repo.get_with_filters(
        post_id=filters.post_id,
        affiliate_id=filters.affiliate_id,
        brand_id=filters.brand_id,
        min_cost=filters.min_cost,
        max_cost=filters.max_cost,
        start_date=filters.start_date,
        end_date=filters.end_date
    )
    
    if not post_costs:
        return PostCostSummaryDTO(
            total_costs=0,
            total_amount=0.0,
            average_cost=0.0,
            min_cost=0.0,
            max_cost=0.0
        )
    
    costs = [cost.cost for cost in post_costs]
    total_costs = len(costs)
    total_amount = sum(costs)
    average_cost = total_amount / total_costs if total_costs > 0 else 0.0
    min_cost = min(costs)
    max_cost = max(costs)
    
    return PostCostSummaryDTO(
        total_costs=total_costs,
        total_amount=total_amount,
        average_cost=average_cost,
        min_cost=min_cost,
        max_cost=max_cost
    )


def handle_get_total_cost_by_affiliate(session: Session, affiliate_id: UUID) -> float:
    """Handle get total cost by affiliate query"""
    repo = PostCostsRepositoryDB(session)
    return repo.get_total_cost_by_affiliate(affiliate_id)


def handle_get_total_cost_by_brand(session: Session, brand_id: UUID) -> float:
    """Handle get total cost by brand query"""
    repo = PostCostsRepositoryDB(session)
    return repo.get_total_cost_by_brand(brand_id)


def handle_get_total_cost_by_post(session: Session, post_id: UUID) -> float:
    """Handle get total cost by post query"""
    repo = PostCostsRepositoryDB(session)
    return repo.get_total_cost_by_post(post_id)
