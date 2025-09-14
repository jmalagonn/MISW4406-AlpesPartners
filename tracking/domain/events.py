from dataclasses import dataclass
from datetime import datetime
import uuid
from seedwork.domain.event_store import Event

@dataclass
class InteractionTracked(Event):
    """
    Evento que se dispara cuando se trackea una interacción
    """
    interaction_id: uuid.UUID
    interaction_type: str
    target_element_id: str
    target_element_type: str
    campaign_id: str
    timestamp: datetime
    
    def __init__(self, interaction_id: uuid.UUID, interaction_type: str, 
                 target_element_id: str, target_element_type: str, 
                 campaign_id: str, timestamp: datetime, 
                 aggregate_id: uuid.UUID = None, version: int = 1):
        super().__init__(aggregate_id or interaction_id, version)
        self.interaction_id = interaction_id
        self.interaction_type = interaction_type
        self.target_element_id = target_element_id
        self.target_element_type = target_element_type
        self.campaign_id = campaign_id
        self.timestamp = timestamp