"""
Queries para operaciones de lectura (CQRS Read Side)
"""
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class InteractionResponse:
    """
    Respuesta de una interacción desde el read model
    """
    id: uuid.UUID
    interaction_type: str
    target_element_id: str
    target_element_type: str
    campaign_id: str
    timestamp: datetime
    created_at: datetime
    updated_on: datetime
