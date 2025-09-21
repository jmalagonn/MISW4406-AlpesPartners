from typing import Optional, List, override
from uuid import UUID
from sqlalchemy import select
from affiliates.domain.repositories import PostsRepository
from affiliates.domain.entities import Post
from affiliates.infrastructure.db.db_models import PostDBModel
from seedwork.domain.entities import Entity
from datetime import datetime

class PostsRepositoryDB(PostsRepository):
    def __init__(self, session):
        self.session = session
    
    @override    
    def add(self, post: Post):
        orm_obj = PostDBModel(
            id=post.id,
            title=post.title,
            content=post.content,
            affiliate_id=post.affiliate_id,
            brand_id=post.brand_id,
            created_at=post.created_at,
            updated_on=post.updated_on,
        )
        self.session.add(orm_obj)
    
    @override    
    def get_by_id(self, post_id: UUID) -> Optional[Post]:
        orm_obj = self.session.get(PostDBModel, post_id)
        if orm_obj:
            return Post(
                id=orm_obj.id,
                title=orm_obj.title,
                content=orm_obj.content,
                affiliate_id=orm_obj.affiliate_id,
                brand_id=orm_obj.brand_id,
                created_at=orm_obj.created_at,
                updated_on=orm_obj.updated_on,
            )
        return None

    @override
    def get_by_affiliate(self, affiliate_id: UUID) -> List[Post]:
        stmt = select(PostDBModel).where(PostDBModel.affiliate_id == affiliate_id)
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Post(
                id=o.id,
                title=o.title,
                content=o.content,
                affiliate_id=o.affiliate_id,
                brand_id=o.brand_id,
                created_at=o.created_at,
                updated_on=o.updated_on,
            )
            for o in orm_objs
        ]

    @override
    def get_all(self) -> List[Post]:
        stmt = (
            select(PostDBModel)
            .order_by(PostDBModel.created_at.desc(), PostDBModel.id.desc())
        )
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Post(
                id=o.id,
                title=o.title,
                content=o.content,
                affiliate_id=o.affiliate_id,
                brand_id=o.brand_id,
                created_at=o.created_at,
                updated_on=o.updated_on,
            )
            for o in orm_objs
        ]
    
    @override
    def update(self, entity: Entity):
        orm_obj = self.session.get(PostDBModel, entity.id)
        if orm_obj:
            orm_obj.title = entity.title
            orm_obj.content = entity.content
            orm_obj.affiliate_id = entity.affiliate_id
            orm_obj.brand_id = entity.brand_id
            orm_obj.updated_on = datetime.now()
            self.session.add(orm_obj)

    @override
    def delete(self, entity_id: UUID):
        orm_obj = self.session.get(PostDBModel, entity_id)
        if orm_obj:
            self.session.delete(orm_obj)