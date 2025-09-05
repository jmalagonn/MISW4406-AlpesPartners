from typing import Optional, List
from sqlalchemy import select
from afiliates.infrastructure.db.db_models import AfiliateModel
from domain.models import Afiliate

class AfiliateRepository:
    def __init__(self, session):
        self.session = session

    def add(self, afiliate: Afiliate):
        orm_obj = AfiliateModel(id=afiliate.id, name=afiliate.name, created_at=afiliate.created_on)
        self.session.add(orm_obj)
        
    def get(self, afiliate_id: str) -> Optional[Afiliate]:
        orm_obj = self.session.get(AfiliateModel, afiliate_id)
        if orm_obj:
            return Afiliate(id=orm_obj.id, name=orm_obj.name, created_at=orm_obj.created_at)
        return None

    def list(self, limit: int = 50, offset: int = 0) -> List[Afiliate]:
        stmt = select(AfiliateModel).order_by(AfiliateModel.created_at.desc()).limit(limit).offset(offset)
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Afiliate(id=obj.id, name=obj.name, created_at=obj.created_at)
            for obj in orm_objs
        ]
