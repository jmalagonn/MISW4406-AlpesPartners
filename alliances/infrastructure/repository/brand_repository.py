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
        orm_obj = BrandDBModel(id=brand.id, name=str(brand.name), created_at=brand.created_at)
        self.session.add(orm_obj)
    
    @override    
    def get_by_id(self, brand_id: str) -> Optional[Brand]:
        orm_obj = self.session.get(BrandDBModel, brand_id)
        if orm_obj:
            return Brand(id=orm_obj.id, name=orm_obj.name, created_at=orm_obj.created_at)
        return None

    @override
    def get_all(self) -> List[Brand]:
        stmt = select(BrandDBModel).order_by(BrandDBModel.created_at.desc())
        orm_objs = self.session.execute(stmt).scalars().all()
        return [Brand(id=o.id, name=o.name, created_at=o.created_at) for o in orm_objs]
    

    @override
    def update(self, entity: Entity):
        ...

    @override
    def delete(self, entity_id: UUID):
        ...