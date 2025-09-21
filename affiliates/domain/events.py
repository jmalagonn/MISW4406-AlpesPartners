import uuid
from dataclasses import dataclass, field
from datetime import datetime
from .rules import IdentityIdIsInmutable
from .exceptions import IdMustBeImmutableException

@dataclass
class DomainEvent():
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    event_date: datetime = field(default=datetime.now())


    @classmethod
    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not IdentityIdIsInmutable(self).is_valid():
            raise IdMustBeImmutableException()
        self._id = self.next_id()
        

@dataclass
class AffiliateCreatedEvent(DomainEvent):
    affiliate_id: uuid.UUID
    name: str
    email: str
    program_id: uuid.UUID
    created_at: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class AffiliateActivatedEvent(DomainEvent):
    affiliate_id: uuid.UUID
    activated_at: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class AffiliateSuspendedEvent(DomainEvent):
    affiliate_id: uuid.UUID
    reason: str = "No reason provided"
    suspended_at: datetime = field(default_factory=lambda: datetime.now())

@dataclass
class PostCreatedEvent(DomainEvent):
    post_id: uuid.UUID
    title: str
    content: str
    affiliate_id: uuid.UUID
    brand_id: uuid.UUID
    created_at: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class PostUpdatedEvent(DomainEvent):
    post_id: uuid.UUID
    content: str
    updated_at: datetime = field(default_factory=lambda: datetime.now())