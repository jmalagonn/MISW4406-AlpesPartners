from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from domain.models import Interaction
from domain.value_objects import InteractionType, TargetElement, CampaignId
from infrastructure.repository import InteractionRepository


@dataclass
class TrackInteraction:
    interaction_type: str
    target_element_id: str
    target_element_type: str
    campaign_id: str
    timestamp: Optional[datetime] = None


def handle_track_interaction(cmd: TrackInteraction, session) -> str:
    """
    Handler para el comando TrackInteraction
    Crea una nueva interacción y la persiste
    """
    # Value objects
    interaction_type = InteractionType(cmd.interaction_type)
    target_element = TargetElement(cmd.target_element_id, cmd.target_element_type)
    campaign_id = CampaignId(cmd.campaign_id)
    
    interaction = Interaction(
        id=Interaction.next_id(),
        interaction_type=interaction_type,
        target_element=target_element,
        campaign_id=campaign_id,
        timestamp=cmd.timestamp or datetime.now()
    )
    
    
    repo = InteractionRepository(session)
    repo.add(interaction)
    
    return str(interaction.id)
