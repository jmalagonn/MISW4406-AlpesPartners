from typing import List
from domain.models import Interaction
from infrastructure.db.db_models import InteractionModel


class InteractionRepository:
    def __init__(self, session):
        self.session = session

    def add(self, interaction: Interaction):
        # Convertir entidad de dominio a modelo de BD
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

    def list(self, limit: int = 50, offset: int = 0) -> List[Interaction]:
        db_models = self.session.query(InteractionModel).limit(limit).offset(offset).all()
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