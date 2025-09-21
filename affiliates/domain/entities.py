from dataclasses import dataclass, field
import uuid
from datetime import datetime
from seedwork.domain.entities import Entity, RootAggregate


@dataclass
class Affiliate(Entity):

    name: str = field(default_factory="")
    email: str = field(default_factory="")
    program_id: uuid.UUID = field(default=None)
    status: str = field(default="pending")
    joined_at: datetime = field(default_factory=lambda: datetime.now())
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_on: datetime = field(default_factory=lambda: datetime.now())
    events: list = field(default_factory=list, init=False)

    def rename(self, new_name: str):
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("Affiliate name too short")
        self.name = new_name.strip()
        self.updated_on = datetime.now()

    def activate(self):
        if self.status == "active":
            raise ValueError("Affiliate already active")
        self.status = "active"
        self.updated_on = datetime.now()

    def suspend(self):
        if self.status != "active":
            raise ValueError("Only active affiliates can be suspended")
        self.status = "suspended"
        self.updated_on = datetime.now()

    def add_event(self, event):
        self.events.append(event)


@dataclass
class Post(RootAggregate):
    id: uuid.UUID = field(default=None)
    title: str = field(default=None)
    content: str = field(default=None)
    affiliate_id: uuid.UUID = field(default=None)
    brand_id: uuid.UUID = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_on: datetime = field(default_factory=lambda: datetime.now())
    events: list = field(default_factory=list, init=False)

    def create_post(self, title: str, content: str, affiliate_id: uuid.UUID, brand_id: uuid.UUID):
        self.title = title
        self.content = content
        self.affiliate_id = affiliate_id
        self.brand_id = brand_id
        self.updated_on = datetime.now()

    def update_content(self, new_content: str):
        if not new_content or len(new_content.strip()) < 5:
            raise ValueError("Content too short")
        self.content = new_content.strip()
        self.updated_on = datetime.now()

    def add_event(self, event):
        self.events.append(event)