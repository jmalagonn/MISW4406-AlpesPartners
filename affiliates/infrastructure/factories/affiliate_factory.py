from dataclasses import dataclass
from sqlalchemy.orm import Session
from affiliates.domain.repositories import AffiliateRepository
from affiliates.infrastructure.repository import AffiliateRepositoryDB
from seedwork.domain.exceptions import FactoryException
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository


@dataclass
class RepositoryFactory(Factory):
    session: Session
          
    def create_object(self, obj_type: type) -> Repository:
        if obj_type == AffiliateRepository:
            return AffiliateRepositoryDB(self.session)
        else:
            raise FactoryException()