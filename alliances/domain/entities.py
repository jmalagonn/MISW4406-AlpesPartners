from datetime import datetime
import uuid
from dataclasses import dataclass, field
from seedwork.domain.entities import Entity


@dataclass
class Brand(Entity):
    id: uuid.UUID = field(hash=True, default=None)
    name: str = field(default="")
    created_at: datetime = field(default=datetime.now())        

    def rename(self, new_name: str):
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("Brand name too short")
          
        self.name = new_name.strip()