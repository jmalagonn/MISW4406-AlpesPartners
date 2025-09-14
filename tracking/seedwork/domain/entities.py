import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Entity(ABC):
    """
    Clase base para todas las entidades del dominio
    """
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    _events: List = field(default_factory=list, init=False, repr=False)
    
    id: uuid.UUID = field(hash=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)
    updated_on: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)

    @classmethod
    def next_id(cls) -> uuid.UUID:
        """
        Genera un nuevo ID único
        """
        return uuid.uuid4()

    @property
    def id(self):
        return self._id
    
    @property
    def events(self):
        return self._events

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if hasattr(self, '_id') and self._id:
            raise ValueError("Entity ID cannot be changed once set")
        self._id = id or self.next_id()
    
    def add_event(self, event):
        """
        Agrega un evento de dominio a la entidad
        """
        self._events.append(event)
    
    def clear_events(self):
        """
        Limpia todos los eventos de dominio
        """
        self._events.clear()
