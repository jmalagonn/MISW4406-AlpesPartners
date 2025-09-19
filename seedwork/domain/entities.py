import uuid
from dataclasses import dataclass, field
from datetime import datetime
from seedwork.domain.events import DomainEvent
from seedwork.domain.mixins import ValidateRulesMixin
from seedwork.domain.rules import EntityIdIsImmutable
from seedwork.domain.exceptions import IdMustBeImmutableException

@dataclass
class Entity:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    created_on: datetime =  field(default=datetime.now())
    updated_on: datetime = field(default=datetime.now())

    @classmethod
    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not EntityIdIsImmutable(self).is_valid():
            raise IdMustBeImmutableException()
        self._id = self.next_id()
        
        
@dataclass
class RootAggregate(Entity, ValidateRulesMixin):
    events: list[DomainEvent] = field(default_factory=list)
    compensation_events: list[DomainEvent] = field(default_factory=list)

    def add_event(self, event: DomainEvent, compansation_event: DomainEvent = None):
        self.events.append(event)

        if compansation_event:
            self.compensation_events.append(compansation_event)
    
    def clean_events(self):
        self.events = list()
        self.compensation_events = list()