"""
Query handlers para operaciones de lectura (CQRS Read Side)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from .queries import InteractionResponse
from infrastructure.db.db_models import InteractionReadModel

class InteractionQueryHandler:
    """
    Handler para queries de interacciones desde el read model
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_interaction_by_id(self, interaction_id: uuid.UUID) -> Optional[InteractionResponse]:
        """
        Obtiene una interacción por ID desde el read model
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
    
    def get_all_interactions(self) -> List[InteractionResponse]:
        """
        Obtiene todas las interacciones desde el read model
        """
        interactions = self.session.query(InteractionReadModel).order_by(
            InteractionReadModel.timestamp.desc()
        ).all()
        
        return [
            InteractionResponse(
                id=interaction.id,
                interaction_type=interaction.interaction_type,
                target_element_id=interaction.target_element_id,
                target_element_type=interaction.target_element_type,
                campaign_id=interaction.campaign_id,
                timestamp=interaction.timestamp,
                created_at=interaction.created_at,
                updated_on=interaction.updated_on
            )
            for interaction in interactions
        ]
    
