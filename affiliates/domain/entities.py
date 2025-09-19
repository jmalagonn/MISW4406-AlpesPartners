from dataclasses import dataclass, field
import uuid
from seedwork.domain.entities import Entity, RootAggregate
from .value_objects import Name


@dataclass
class Affiliate(Entity):
    name: str = field(default_factory="")

    def rename(self, new_name: str):
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("Affiliate name too short")
        self.name = new_name.strip()
        

@dataclass
class Post(RootAggregate):
    title: str = field(default=None)
    content: str = field(default=None)
    affiliate_id: uuid.UUID = field(default=None)
    brand_id: uuid.UUID = field(default=None)
    
    def create_post(self, post: Post):
        self.title = post.title
        self.content = post.content
        self.affiliate_id = post.affiliate_id
        self.brand_id = post.brand_id