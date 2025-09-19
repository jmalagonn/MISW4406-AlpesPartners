from typing import Optional, List, override
from uuid import UUID
from sqlalchemy import select
from affiliates.domain.repositories import PostsRepository
from affiliates.domain.entities import Post
from affiliates.infrastructure.db.db_models import PostDBModel
from seedwork.domain.entities import Entity

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
            brand_id=post.brand_id
        )
        self.session.add(orm_obj)
    
    @override    
    def get_by_id(self, post_id: str) -> Optional[Post]:
        orm_obj = self.session.get(PostDBModel, post_id)
        if orm_obj:
            return Post(id=orm_obj.id, name=orm_obj.name, created_at=orm_obj.created_at)
        return None

    @override
    def get_all(self) -> List[Post]:
        stmt = select(PostDBModel).order_by(PostDBModel.created_at.desc())
        orm_objs = self.session.execute(stmt).scalars().all()
        return [
            Post(
                id=orm.id, 
                title=orm.title, 
                content=orm.content, 
                affiliate_id=orm.affiliate_id, 
                brand_id=orm.brand_id, 
                created_at=orm.created_at) 
            for orm in orm_objs]
    

    @override
    def update(self, entity: Entity):
        ...

    @override
    def delete(self, entity_id: UUID):
        ...
