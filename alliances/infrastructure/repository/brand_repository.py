from typing import Optional, List, override
from uuid import UUID
from sqlalchemy import select
from alliances.domain.repositories import BrandRepository
from alliances.infrastructure.db.db_models import BrandDBModel
from alliances.domain.entities import Brand
from seedwork.domain.entities import Entity


class BrandRepositoryDB(BrandRepository):
    def __init__(self, session):
        self.session = session
    
    @override    
    def add(self, brand: Brand):
        orm_obj = BrandDBModel(
            id=brand.id,
            name=str(brand.name),
            category=brand.category,
            created_at=brand.created_at,
            updated_on=brand.updated_on
        )
        self.session.add(orm_obj)
    
    @override    
    def get_by_id(self, brand_id: UUID) -> Optional[Brand]:
        orm_obj = self.session.get(BrandDBModel, brand_id)
        if orm_obj:
            return Brand(
                id=orm_obj.id,
                name=orm_obj.name,
                category=orm_obj.category,
                created_at=orm_obj.created_at,
                updated_on=orm_obj.updated_on
            )
        return None

    @override
    def get_all(self) -> List[Brand]:
        stmt = select(BrandDBModel).order_by(BrandDBModel.created_at.desc())
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Brand(
                id=o.id,
                name=o.name,
                category=o.category,
                created_at=o.created_at,
                updated_on=o.updated_on
            ) for o in orm_objs
        ]
    
    @override
    def update(self, entity: Brand):
        orm_obj = self.session.get(BrandDBModel, entity.id)
        if orm_obj:
            orm_obj.name = str(entity.name)
            orm_obj.category = entity.category
            orm_obj.updated_on = entity.updated_on
            self.session.add(orm_obj)

    @override
    def delete(self, entity_id: UUID):
        orm_obj = self.session.get(BrandDBModel, entity_id)
        if orm_obj:
            self.session.delete(orm_obj)