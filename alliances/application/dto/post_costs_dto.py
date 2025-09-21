from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID
from datetime import datetime


@dataclass
class PostCostDTO:
    """Data Transfer Object for Post Cost"""
    id: UUID
    post_id: UUID
    affiliate_id: UUID
    brand_id: UUID
    cost: float
    created_at: datetime

    @classmethod
    def from_db_model(cls, db_model) -> 'PostCostDTO':
        """Create DTO from database model"""
        return cls(
            id=db_model.id,
            post_id=db_model.post_id,
            affiliate_id=db_model.affiliate_id,
            brand_id=db_model.brand_id,
            cost=db_model.cost,
            created_at=db_model.created_at
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "post_id": str(self.post_id),
            "affiliate_id": str(self.affiliate_id),
            "brand_id": str(self.brand_id),
            "cost": self.cost,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class PostCostSummaryDTO:
    """Data Transfer Object for Post Cost Summary"""
    total_costs: int
    total_amount: float
    average_cost: float
    min_cost: float
    max_cost: float

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "total_costs": self.total_costs,
            "total_amount": self.total_amount,
            "average_cost": self.average_cost,
            "min_cost": self.min_cost,
            "max_cost": self.max_cost
        }


@dataclass
class PostCostFiltersDTO:
    """Data Transfer Object for Post Cost Filters"""
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

    @classmethod
    def from_request_args(cls, args) -> 'PostCostFiltersDTO':
        """Create DTO from Flask request arguments"""
        return cls(
            post_id=args.get('post_id'),
            affiliate_id=args.get('affiliate_id'),
            brand_id=args.get('brand_id'),
            min_cost=float(args.get('min_cost')) if args.get('min_cost') else None,
            max_cost=float(args.get('max_cost')) if args.get('max_cost') else None,
            start_date=args.get('start_date'),
            end_date=args.get('end_date'),
            order_by=args.get('order_by', 'created_at'),
            order_direction=args.get('order_direction', 'desc'),
            limit=int(args.get('limit')) if args.get('limit') else None,
            offset=int(args.get('offset')) if args.get('offset') else None
        )


@dataclass
class PostCostResponseDTO:
    """Data Transfer Object for Post Cost API Response"""
    data: List[PostCostDTO]
    total_count: int
    page: int
    page_size: int
    total_pages: int

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "data": [cost.to_dict() for cost in self.data],
            "pagination": {
                "total_count": self.total_count,
                "page": self.page,
                "page_size": self.page_size,
                "total_pages": self.total_pages
            }
        }
