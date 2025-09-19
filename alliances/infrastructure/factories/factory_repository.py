from dataclasses import dataclass
from alliances.domain.repositories import BrandRepository
from alliances.infrastructure.repository.brand_repository import BrandRepositoryDB
from seedwork.domain.exceptions import FactoryException
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository


@dataclass
class FactoryRepository(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == BrandRepository.__class__:
            return BrandRepositoryDB()
        else:
            raise FactoryException()