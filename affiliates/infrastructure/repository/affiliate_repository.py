from typing import Optional, List, override
from uuid import UUID
from sqlalchemy import select
from affiliates.domain.entities import Affiliate
from affiliates.infrastructure.db.db_models import AffiliateDBModel
from affiliates.domain.repositories import AffiliateRepository
from seedwork.domain.entities import Entity

class AffiliateRepositoryDB(AffiliateRepository):
    def __init__(self, session):
        self.session = session
    
    @override    
    def add(self, Affiliate: Affiliate):
        orm_obj = AffiliateDBModel(id=Affiliate.id, name=str(Affiliate.name), created_at=Affiliate.created_at)
        self.session.add(orm_obj)
    
    @override    
    def get_by_id(self, Affiliate_id: str) -> Optional[Affiliate]:
        orm_obj = self.session.get(AffiliateDBModel, Affiliate_id)
        if orm_obj:
            return Affiliate(id=orm_obj.id, name=orm_obj.name, created_at=orm_obj.created_at)
        return None

    @override
    def get_all(self) -> List[Affiliate]:
        stmt = select(AffiliateDBModel).order_by(AffiliateDBModel.created_at.desc())
        orm_objs = self.session.execute(stmt).scalars().all()
        return [Affiliate(id=o.id, name=o.name, created_at=o.created_at) for o in orm_objs]
    

    @override
    def update(self, entity: Entity):
        ...

    @override
    def delete(self, entity_id: UUID):
        ...
