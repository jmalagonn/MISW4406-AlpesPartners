"""
Query para obtener una interacción por ID
"""
from typing import Optional
from sqlalchemy.orm import Session
import uuid

from .queries import InteractionResponse
from infrastructure.db.db_models import InteractionReadModel

class GetInteractionByIdQuery:
    """
    Query para obtener una interacción específica por ID desde el read model
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def execute(self, interaction_id: uuid.UUID) -> Optional[InteractionResponse]:
        """
        Ejecuta la query para obtener una interacción por ID
        """
        interaction = self.session.query(InteractionReadModel).filter(
            InteractionReadModel.id == interaction_id
        ).first()
        
        if not interaction:
            return None
        
        return InteractionResponse(
            id=interaction.id,
            interaction_type=interaction.interaction_type,
            target_element_id=interaction.target_element_id,
            target_element_type=interaction.target_element_type,
            campaign_id=interaction.campaign_id,
            timestamp=interaction.timestamp,
            created_at=interaction.created_at,
            updated_on=interaction.updated_on
        )
