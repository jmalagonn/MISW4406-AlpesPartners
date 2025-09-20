from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models import Interaction
from infrastructure.db.db_models import InteractionModel, InteractionReadModel


class InteractionRepository:
    """
    Repositorio para el write model (tabla interactions)
    """
    def __init__(self, session: Session):
        self.session = session

    def add(self, interaction: Interaction):
        
        db_model = InteractionModel(
            id=interaction.id,
            interaction_type=interaction.interaction_type.value,
            target_element_id=interaction.target_element.element_id,
            target_element_type=interaction.target_element.element_type,
            campaign_id=interaction.campaign_id.value,
            timestamp=interaction.timestamp,
            created_at=interaction.created_at,
            updated_on=interaction.updated_on
        )
        self.session.add(db_model)
        

    def get(self, interaction_id: str) -> Interaction:
        db_model = self.session.get(InteractionModel, interaction_id)
        if db_model:
            return self._db_model_to_entity(db_model)
        return None
    
    
    def get_interations_by_post_id(self, post_id: str, start_date: Optional[datetime], end_date: Optional[datetime]):
        query = self.session.query(InteractionModel).filter(InteractionModel.campaign_id == post_id)
        
        if start_date is not None:
            query = query.filter(InteractionModel.created_at >= start_date)
        if end_date is not None:
            query = query.filter(InteractionModel.created_at < end_date)
            
        return [self._db_model_to_entity(model) for model in query]
    

    def list(self) -> List[Interaction]:
        db_models = self.session.query(InteractionModel).all()
        return [self._db_model_to_entity(model) for model in db_models]
    
    
    def _db_model_to_entity(self, db_model: InteractionModel) -> Interaction:
        """Convierte modelo de BD a entidad de dominio"""
        from domain.value_objects import InteractionType, TargetElement, CampaignId
        
        return Interaction(
            id=db_model.id,
            interaction_type=InteractionType(db_model.interaction_type),
            target_element=TargetElement(db_model.target_element_id, db_model.target_element_type),
            campaign_id=CampaignId(db_model.campaign_id),
            timestamp=db_model.timestamp,
            created_at=db_model.created_at,
            updated_on=db_model.updated_on
        )


class InteractionReadRepository:
    """
    Repositorio para consultas optimizadas del read model
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, interaction_id: str) -> Optional[InteractionReadModel]:
        """
        Obtiene una interacción por su ID
        """
        return self.session.get(InteractionReadModel, interaction_id)
    
       
    def get_all(self) -> List[InteractionReadModel]:
        """
        Obtiene todas las interacciones
        """
        return self.session.query(InteractionReadModel).all()
    
