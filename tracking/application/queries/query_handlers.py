"""
Query handlers para operaciones de lectura (CQRS Read Side)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from .queries import InteractionResponse
from .get_interaction_by_id import GetInteractionByIdQuery
from .get_all_interactions import GetAllInteractionsQuery

class InteractionQueryHandler:
    """
    Handler principal que orquesta las queries de interacciones
    """
    
    def __init__(self, session: Session):
        self.session = session
        # Inicializar las queries específicas
        self.get_interaction_by_id_query = GetInteractionByIdQuery(session)
        self.get_all_interactions_query = GetAllInteractionsQuery(session)
    
    def get_interaction_by_id(self, interaction_id: uuid.UUID) -> Optional[InteractionResponse]:
        """
        Obtiene una interacción por ID desde el read model
        """
        return self.get_interaction_by_id_query.execute(interaction_id)
    
    def get_all_interactions(self) -> List[InteractionResponse]:
        """
        Obtiene todas las interacciones desde el read model
        """
        return self.get_all_interactions_query.execute()
    
