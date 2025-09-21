from dataclasses import dataclass, field
from datetime import datetime
import uuid
from seedwork.domain.entities import Entity


@dataclass
class Brand(Entity):
    id: uuid.UUID = field(default_factory=uuid.uuid4, hash=True)
    name: str = field(default_factory=str)
    category: str = field(default_factory=lambda: "general")
    created_at: datetime = field(default_factory=datetime.now)
    updated_on: datetime = field(default_factory=datetime.now)
    events: list = field(default_factory=list, init=False)

    def rename(self, new_name: str):
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("Brand name too short")
        self.name = new_name.strip()
        self.updated_on = datetime.now()

    def add_event(self, event):
        self.events.append(event)

    def update_timestamp(self):
        self.updated_on = datetime.now()