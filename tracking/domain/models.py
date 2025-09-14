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
    
    