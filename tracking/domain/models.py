from dataclasses import dataclass, field
from datetime import datetime
from domain.value_objects import InteractionType, TargetElement, CampaignId
import uuid


@dataclass
class Interaction:
    """
    Entidad de dominio para interacciones
    """
    interaction_type: InteractionType
    target_element: TargetElement
    campaign_id: CampaignId
    timestamp: datetime = field(default_factory=lambda: datetime.now())
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_on: datetime = field(default_factory=lambda: datetime.now())
    events: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        """
        Inicialización del aggregate
        """
        self._track_interaction()
    
    def _track_interaction(self) -> None:
        """
        Dispara el evento de dominio InteractionTracked
        """
        from domain.events import InteractionTracked
        
        event = InteractionTracked(
            interaction_id=self.id,
            interaction_type=self.interaction_type.value,
            target_element_id=self.target_element.element_id,
            target_element_type=self.target_element.element_type,
            campaign_id=self.campaign_id.value,
            timestamp=self.timestamp,
            aggregate_id=self.id,
            version=1
        )
        
        self.add_event(event)
    
    def add_event(self, event):
        """
        Agrega un evento de dominio a la entidad
        """
        self.events.append(event)
    
    