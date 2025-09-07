from typing import Optional, List
from sqlalchemy import select
from infrastructure.db.db_models import AffiliateModel
from domain.models import Affiliate

class AffiliateRepository:
    def __init__(self, session):
        self.session = session

    def add(self, affiliate: Affiliate):
        orm_obj = AffiliateModel(id=affiliate.id, name=str(affiliate.name), created_at=affiliate.created_at)
        self.session.add(orm_obj)
        
    def get(self, affiliate_id: str) -> Optional[Affiliate]:
        orm_obj = self.session.get(AffiliateModel, affiliate_id)
        if orm_obj:
            return Affiliate(id=orm_obj.id, name=orm_obj.name, created_at=orm_obj.created_at)
        return None

    def list(self, limit: int = 50, offset: int = 0) -> List[Affiliate]:
        stmt = select(AffiliateModel).order_by(AffiliateModel.created_at.desc()).limit(limit).offset(offset)
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Affiliate(id=obj.id, name=obj.name, created_at=obj.created_at)
            for obj in orm_objs
        ]
