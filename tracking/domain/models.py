import uuid
from dataclasses import dataclass, field
from datetime import datetime
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