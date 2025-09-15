from typing import List
from sqlalchemy.orm import Session
from seedwork.domain.projection import Projection
from domain.events import InteractionTracked

class ProjectionHandler:
    """
    Handler que procesa eventos y actualiza las proyecciones
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.projections = self._register_projections()
    
    def _register_projections(self) -> List[Projection]:
        """
        Registra todas las proyecciones disponibles
        """
        from infrastructure.projections.interaction_projection import InteractionProjection
        
        return [
            InteractionProjection(self.session)
        ]
    
    def handle_event(self, event) -> None:
        """
        Procesa un evento y actualiza todas las proyecciones relevantes
        """
        for projection in self.projections:
            if self._should_handle_event(projection, event):
                projection.handle_event(event)
    
    def _should_handle_event(self, projection: Projection, event) -> bool:
        """
        Determina si una proyección debe procesar un evento específico
        """
        return True
    
