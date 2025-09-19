import logging
from dataclasses import asdict, dataclass
from typing import override
from affiliates.application.dto import PostDTO
from affiliates.application.mappers import PostMapper
from affiliates.domain.entities import Post
from affiliates.domain.factories import PostFactory
from affiliates.domain.repositories import PostsRepository
from affiliates.infrastructure.factories import RepositoryFactory
from seedwork.application.commands import Command, CommandHandler


@dataclass
class CreatePost(Command):
    title: str
    content: str
    affiliate_id: str
    brand_id: str
    

class CreatePostHandler(CommandHandler):
    def __init__(self, session):
        self.session = session
        self.repository_factory: RepositoryFactory = RepositoryFactory(session = session)
        self.post_factory: PostFactory = PostFactory()
        
    @override
    def handle(self, command: CreatePost):
        logging.info("Received command=%s", asdict(command))
        
        brand_dto = PostDTO(
            title=command.title,
            content=command.content,
            affiliate_id=command.affiliate_id,
            brand_id=command.brand_id
        )
        
        repo: PostsRepository = self.repository_factory.create_object(PostsRepository)
        post: Post = self.post_factory.create_object(brand_dto, PostMapper())
        
        repo.add(post)
        self.session.commit()
        
        logging.info("Affiliate created with id=%s", post.id)