from abc import ABC, abstractmethod
from typing import List
import uuid

class Event(ABC):
    """
    Clase base para todos los eventos de dominio
    """
    def __init__(self, aggregate_id: uuid.UUID, version: int = 1):
        self.aggregate_id = aggregate_id
        self.version = version
        self.created_at = None

class EventStore(ABC):
    """
    Interfaz base para el Event Store
    """
    
    @abstractmethod
    def save_events(self, aggregate_id: uuid.UUID, events: List[Event], expected_version: int) -> None:
        """
        Guarda eventos para un aggregate
        """
        pass
    
    @abstractmethod
    def get_events(self, aggregate_id: uuid.UUID) -> List[Event]:
        """
        Obtiene todos los eventos de un aggregate
        """
        pass
