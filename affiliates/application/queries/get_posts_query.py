import logging
from affiliates.domain.factories import PostFactory
from affiliates.domain.repositories import PostsRepository
from affiliates.infrastructure.factories import RepositoryFactory



class GetPostsQueryHandler:
    def __init__(self, session):
        self.session = session
        self.repository_factory: RepositoryFactory = RepositoryFactory(session = session)
        self.post_factory: PostFactory = PostFactory()

    def handle(self):
        logging.info("Listing posts")
        
        repo: PostsRepository = self.repository_factory.create_object(PostsRepository)
        posts = repo.get_all()
        
        return posts