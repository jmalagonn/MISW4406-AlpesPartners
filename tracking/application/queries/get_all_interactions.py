"""
Query para obtener todas las interacciones
"""
from typing import List
from sqlalchemy.orm import Session

from .queries import InteractionResponse
from infrastructure.db.db_models import InteractionReadModel

class GetAllInteractionsQuery:
    """
    Query para obtener todas las interacciones desde el read model
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def execute(self) -> List[InteractionResponse]:
        """
        Ejecuta la query para obtener todas las interacciones
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
