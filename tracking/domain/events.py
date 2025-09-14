from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class InteractionTrackedEvent:
    interaction_id: uuid.UUID
    interaction_type: str
    target_element_id: str
    target_element_type: str
    campaign_id: str
    timestamp: datetime
