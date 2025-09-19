from dataclasses import dataclass
from sqlalchemy.orm import Session
from alliances.domain.repositories import BrandRepository
from alliances.infrastructure.repository.brand_repository import BrandRepositoryDB
from seedwork.domain.exceptions import FactoryException
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository


@dataclass
class RepositoryFactory(Factory):
    session: Session
          
    def create_object(self, obj_type: type) -> Repository:
        if obj_type == BrandRepository:
            return BrandRepositoryDB(self.session)
        else:
            raise FactoryException()