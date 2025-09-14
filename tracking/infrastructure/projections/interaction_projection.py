from sqlalchemy.orm import Session
from seedwork.domain.projection import Projection
from domain.events import InteractionTracked
from infrastructure.db.db_models import InteractionModel, InteractionReadModel

class InteractionProjection(Projection):
    """
    Proyección que mantiene la tabla interactions sincronizada con los eventos
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def handle_event(self, event: InteractionTracked) -> None:
        """
        Procesa el evento InteractionTracked y actualiza ambas proyecciones
        """

        self._update_main_table(event)
        

        self._update_read_model(event)
    
    def _update_main_table(self, event: InteractionTracked) -> None:
        """
        Actualiza la tabla principal interactions
        """
        interaction_model = InteractionModel(
            id=event.interaction_id,
            interaction_type=event.interaction_type,
            target_element_id=event.target_element_id,
            target_element_type=event.target_element_type,
            campaign_id=event.campaign_id,
            timestamp=event.timestamp,
            created_at=event.created_at,
            updated_on=event.created_at
        )
        
        # si ya existe
        existing = self.session.get(InteractionModel, event.interaction_id)
        if existing:
            # Actualizar
            existing.interaction_type = event.interaction_type
            existing.target_element_id = event.target_element_id
            existing.target_element_type = event.target_element_type
            existing.campaign_id = event.campaign_id
            existing.timestamp = event.timestamp
            existing.updated_on = event.created_at
        else:
            # Crear
            self.session.add(interaction_model)
    
    def _update_read_model(self, event: InteractionTracked) -> None:
        """
        Actualiza el read model optimizado para queries
        """
        read_model = InteractionReadModel(
            id=event.interaction_id,
            interaction_type=event.interaction_type,
            target_element_id=event.target_element_id,
            target_element_type=event.target_element_type,
            campaign_id=event.campaign_id,
            timestamp=event.timestamp,
            created_at=event.created_at,
            updated_on=event.created_at
        )
        
        
        existing = self.session.get(InteractionReadModel, event.interaction_id)
        if existing:
            # Actualizar
            existing.interaction_type = event.interaction_type
            existing.target_element_id = event.target_element_id
            existing.target_element_type = event.target_element_type
            existing.campaign_id = event.campaign_id
            existing.timestamp = event.timestamp
            existing.updated_on = event.created_at
        else:
            # Crear
            self.session.add(read_model)
    
    def get_projection_name(self) -> str:
        return "interactions_projection"
