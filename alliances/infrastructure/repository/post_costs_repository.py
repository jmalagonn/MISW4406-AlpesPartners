from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from alliances.infrastructure.db.db_models import PostCostsDBModel


class PostCostsRepositoryDB:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[PostCostsDBModel]:
        """Get all post costs"""
        return self.session.query(PostCostsDBModel).all()

    def get_by_id(self, cost_id: UUID) -> Optional[PostCostsDBModel]:
        """Get post cost by ID"""
        return self.session.query(PostCostsDBModel).filter(PostCostsDBModel.id == cost_id).first()

    def get_by_post_id(self, post_id: UUID) -> List[PostCostsDBModel]:
        """Get all post costs for a specific post"""
        return self.session.query(PostCostsDBModel).filter(PostCostsDBModel.post_id == post_id).all()

    def get_by_affiliate_id(self, affiliate_id: UUID) -> List[PostCostsDBModel]:
        """Get all post costs for a specific affiliate"""
        return self.session.query(PostCostsDBModel).filter(PostCostsDBModel.affiliate_id == affiliate_id).all()

    def get_by_brand_id(self, brand_id: UUID) -> List[PostCostsDBModel]:
        """Get all post costs for a specific brand"""
        return self.session.query(PostCostsDBModel).filter(PostCostsDBModel.brand_id == brand_id).all()

    def get_by_affiliate_and_brand(self, affiliate_id: UUID, brand_id: UUID) -> List[PostCostsDBModel]:
        """Get post costs for a specific affiliate and brand combination"""
        return self.session.query(PostCostsDBModel).filter(
            and_(
                PostCostsDBModel.affiliate_id == affiliate_id,
                PostCostsDBModel.brand_id == brand_id
            )
        ).all()

    def get_by_cost_range(self, min_cost: float, max_cost: float) -> List[PostCostsDBModel]:
        """Get post costs within a specific cost range"""
        return self.session.query(PostCostsDBModel).filter(
            and_(
                PostCostsDBModel.cost >= min_cost,
                PostCostsDBModel.cost <= max_cost
            )
        ).all()

    def get_by_date_range(self, start_date, end_date) -> List[PostCostsDBModel]:
        """Get post costs within a specific date range"""
        return self.session.query(PostCostsDBModel).filter(
            and_(
                PostCostsDBModel.created_at >= start_date,
                PostCostsDBModel.created_at <= end_date
            )
        ).all()

    def get_ordered_by_cost(self, ascending: bool = True) -> List[PostCostsDBModel]:
        """Get post costs ordered by cost amount"""
        order_func = asc if ascending else desc
        return self.session.query(PostCostsDBModel).order_by(order_func(PostCostsDBModel.cost)).all()

    def get_ordered_by_date(self, ascending: bool = True) -> List[PostCostsDBModel]:
        """Get post costs ordered by creation date"""
        order_func = asc if ascending else desc
        return self.session.query(PostCostsDBModel).order_by(order_func(PostCostsDBModel.created_at)).all()

    def get_with_filters(
        self,
        post_id: Optional[UUID] = None,
        affiliate_id: Optional[UUID] = None,
        brand_id: Optional[UUID] = None,
        min_cost: Optional[float] = None,
        max_cost: Optional[float] = None,
        start_date = None,
        end_date = None,
        order_by: str = "created_at",
        order_direction: str = "desc",
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[PostCostsDBModel]:
        """Get post costs with multiple filters and pagination"""
        query = self.session.query(PostCostsDBModel)
        
        # Apply filters
        filters = []
        
        if post_id:
            filters.append(PostCostsDBModel.post_id == post_id)
        if affiliate_id:
            filters.append(PostCostsDBModel.affiliate_id == affiliate_id)
        if brand_id:
            filters.append(PostCostsDBModel.brand_id == brand_id)
        if min_cost is not None:
            filters.append(PostCostsDBModel.cost >= min_cost)
        if max_cost is not None:
            filters.append(PostCostsDBModel.cost <= max_cost)
        if start_date:
            filters.append(PostCostsDBModel.created_at >= start_date)
        if end_date:
            filters.append(PostCostsDBModel.created_at <= end_date)
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Apply ordering
        if order_by == "cost":
            order_column = PostCostsDBModel.cost
        elif order_by == "created_at":
            order_column = PostCostsDBModel.created_at
        else:
            order_column = PostCostsDBModel.created_at
        
        if order_direction.lower() == "asc":
            query = query.order_by(asc(order_column))
        else:
            query = query.order_by(desc(order_column))
        
        # Apply pagination
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        return query.all()

    def get_total_cost_by_affiliate(self, affiliate_id: UUID) -> float:
        """Get total cost for a specific affiliate"""
        result = self.session.query(PostCostsDBModel.cost).filter(
            PostCostsDBModel.affiliate_id == affiliate_id
        ).all()
        return sum(row.cost for row in result)

    def get_total_cost_by_brand(self, brand_id: UUID) -> float:
        """Get total cost for a specific brand"""
        result = self.session.query(PostCostsDBModel.cost).filter(
            PostCostsDBModel.brand_id == brand_id
        ).all()
        return sum(row.cost for row in result)

    def get_total_cost_by_post(self, post_id: UUID) -> float:
        """Get total cost for a specific post"""
        result = self.session.query(PostCostsDBModel.cost).filter(
            PostCostsDBModel.post_id == post_id
        ).all()
        return sum(row.cost for row in result)

    def count_by_filters(
        self,
        post_id: Optional[UUID] = None,
        affiliate_id: Optional[UUID] = None,
        brand_id: Optional[UUID] = None,
        min_cost: Optional[float] = None,
        max_cost: Optional[float] = None,
        start_date = None,
        end_date = None
    ) -> int:
        """Count post costs with filters"""
        query = self.session.query(PostCostsDBModel)
        
        # Apply filters
        filters = []
        
        if post_id:
            filters.append(PostCostsDBModel.post_id == post_id)
        if affiliate_id:
            filters.append(PostCostsDBModel.affiliate_id == affiliate_id)
        if brand_id:
            filters.append(PostCostsDBModel.brand_id == brand_id)
        if min_cost is not None:
            filters.append(PostCostsDBModel.cost >= min_cost)
        if max_cost is not None:
            filters.append(PostCostsDBModel.cost <= max_cost)
        if start_date:
            filters.append(PostCostsDBModel.created_at >= start_date)
        if end_date:
            filters.append(PostCostsDBModel.created_at <= end_date)
        
        if filters:
            query = query.filter(and_(*filters))
        
        return query.count()
