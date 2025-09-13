from typing import Optional, List
from sqlalchemy import select
from infrastructure.db.db_models import BrandModel
from domain.models import Brand


class BrandRepository:
    def __init__(self, session):
        self.session = session
        
    def add(self, brand: Brand):
        orm_obj = BrandModel(id=brand.id, name=str(brand.name), created_at=brand.created_at)
        self.session.add(orm_obj)
        
    def get(self, brand_id: str) -> Optional[Brand]:
        orm_obj = self.session.get(BrandModel, brand_id)
        if orm_obj:
            return Brand(id=orm_obj.id, name=orm_obj.name, created_at=orm_obj.created_at)
        return None

    def list(self, limit: int = 50, offset: int = 0) -> List[Brand]:
        stmt = select(BrandModel).order_by(BrandModel.created_at.desc()).limit(limit).offset(offset)
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Brand(id=obj.id, name=obj.name, created_at=obj.created_at)
            for obj in orm_objs
        ]