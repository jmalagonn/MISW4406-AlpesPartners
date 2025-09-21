from typing import Optional, List, override
from uuid import UUID
from sqlalchemy import select
from affiliates.domain.entities import Affiliate
from affiliates.infrastructure.db.db_models import AffiliateDBModel
from affiliates.domain.repositories import AffiliateRepository
from seedwork.domain.entities import Entity
from datetime import datetime

class AffiliateRepositoryDB(AffiliateRepository):
    def __init__(self, session):
        self.session = session
    
    @override    
    def add(self, affiliate: Affiliate):
        orm_obj = AffiliateDBModel(
            id=affiliate.id,
            name=affiliate.name,
            email=str(affiliate.email),
            program_id=affiliate.program_id,
            status=affiliate.status,
            joined_at=affiliate.joined_at,
            updated_on=affiliate.updated_on,
            created_at=affiliate.created_at
        )
        self.session.add(orm_obj)
    
    @override    
    def get_by_id(self, affiliate_id: UUID) -> Optional[Affiliate]:
        orm_obj = self.session.get(AffiliateDBModel, affiliate_id)
        if orm_obj:
            return Affiliate(
                id=orm_obj.id,
                name=orm_obj.name,
                email=orm_obj.email,
                program_id=orm_obj.program_id,
                status=orm_obj.status,
                joined_at=orm_obj.joined_at,
                updated_on=orm_obj.updated_on,
            )
        return None

    @override
    def get_all(self) -> List[Affiliate]:
        stmt = select(AffiliateDBModel).order_by(AffiliateDBModel.joined_at.desc())
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Affiliate(
                id=o.id,
                name=o.name,
                email=o.email,
                program_id=o.program_id,
                status=o.status,
                joined_at=o.joined_at,
                updated_on=o.updated_on,
                created_at=o.created_at
            )
            for o in orm_objs
        ]
    
    @override
    def update(self, entity: Entity):
        orm_obj = self.session.get(AffiliateDBModel, entity.id)
        if orm_obj:
            orm_obj.name = entity.name
            orm_obj.email = str(entity.email)
            orm_obj.program_id = entity.program_id
            orm_obj.status = entity.status
            orm_obj.updated_on = datetime.now()
            self.session.add(orm_obj)

    @override
    def delete(self, entity_id: UUID):
        orm_obj = self.session.get(AffiliateDBModel, entity_id)
        if orm_obj:
            self.session.delete(orm_obj)