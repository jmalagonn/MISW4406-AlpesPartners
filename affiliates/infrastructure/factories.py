from dataclasses import dataclass
from sqlalchemy.orm import Session
from affiliates.domain.repositories import AffiliateRepository, PostsRepository
from affiliates.infrastructure.repository.affiliate_repository import AffiliateRepositoryDB
from affiliates.infrastructure.repository.posts_repository import PostsRepositoryDB
from seedwork.domain.exceptions import FactoryException
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository


@dataclass
class RepositoryFactory(Factory):
    session: Session
          
    def create_object(self, obj_type: type) -> Repository:
        if obj_type == AffiliateRepository:
            return AffiliateRepositoryDB(self.session)
        if obj_type == PostsRepository:
            return PostsRepositoryDB(self.session)
        else:
            raise FactoryException()