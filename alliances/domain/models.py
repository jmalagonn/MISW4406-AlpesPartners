import uuid, datetime
from dataclasses import dataclass, field
from domain.value_objects import Name
from domain.exceptions import IdMustBeImmutableException
from domain.rules import IdentityIdIsInmutable


@dataclass
class Entity:
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    _events: list = field(default_factory=list, init=False, repr=False)
    
    id: uuid.UUID = field(hash=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)
    updated_on: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)

    @classmethod
    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id
    
    @property
    def events(self):
        return self._events

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not IdentityIdIsInmutable(self).is_valid():
            raise IdMustBeImmutableException()
        self._id = self.next_id()


@dataclass
class Brand(Entity):
    name: Name = field(default_factory=Name)

    # def __post_init__(self):
    #     from domain.events import AffiliateCreatedEvent
    #     self._events.append(
    #         AffiliateCreatedEvent(
    #             id=self.id,
    #             name=self.name,
    #             created_at=self.created_at
    #         )
    #     )

    def rename(self, new_name: str):
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("Brand name too short")
          
        self.name = new_name.strip()