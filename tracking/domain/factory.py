from dataclasses import dataclass
from typing import Any
from seedwork.domain.factory import Factory
from seedwork.domain.repository import Mapper
from domain.models import Interaction
from domain.rules import (
    InteractionTypeCannotBeEmpty,
    InteractionTypeMustBeValid,
    TargetElementIdCannotBeEmpty,
    TargetElementTypeCannotBeEmpty,
    CampaignIdCannotBeEmpty
)


@dataclass
class InteractionFactory(Factory):
    """
    Factory específica para crear objetos Interaction
    """
    
    def create_object(self, obj: Any, mapper: Mapper = None) -> Any:
        if isinstance(obj, Interaction):
            # Si es una entidad, convertir a DTO
            if mapper is None:
                mapper = InteractionMapper()
            return mapper.entity_to_dto(obj)
        else:
            # Si es un DTO, crear entidad
            print("Fabricando interacción: ", obj)
            
            try:
                if mapper is None:
                    mapper = InteractionMapper()
                print("Mapper creado correctamente")
                
                interaction: Interaction = mapper.dto_to_entity(obj)
                print("Entidad creada correctamente")
                
                # Validar todas las reglas de negocio
                print("Validando reglas de negocio...")
                self.validate_rule(InteractionTypeCannotBeEmpty(interaction.interaction_type.value))
                self.validate_rule(InteractionTypeMustBeValid(interaction.interaction_type.value))
                self.validate_rule(TargetElementIdCannotBeEmpty(interaction.target_element.element_id))
                self.validate_rule(TargetElementTypeCannotBeEmpty(interaction.target_element.element_type))
                self.validate_rule(CampaignIdCannotBeEmpty(interaction.campaign_id.value))
                
                print("Reglas de negocio validadas correctamente")
                return interaction
                
            except Exception as e:
                print(f"Error en factory: {str(e)}")
                print(f"Tipo de error: {type(e)}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                raise


class InteractionMapper(Mapper):
    """
    Mapeador específico para Interaction
    """
    
    def dto_to_entity(self, dto: dict) -> Interaction:
        """
        Convierte DTO a entidad Interaction
        """
        from domain.value_objects import InteractionType, TargetElement, CampaignId
        from datetime import datetime
        import uuid
        
        return Interaction(
            interaction_type=InteractionType(dto['interaction_type']),
            target_element=TargetElement(dto['target_element_id'], dto['target_element_type']),
            campaign_id=CampaignId(dto['campaign_id']),
            timestamp=dto.get('timestamp', datetime.now())
        )
    
    def entity_to_dto(self, entity: Interaction) -> dict:
        """
        Convierte entidad Interaction a DTO
        """
        return {
            'id': str(entity.id),
            'interaction_type': entity.interaction_type.value,
            'target_element_id': entity.target_element.element_id,
            'target_element_type': entity.target_element.element_type,
            'campaign_id': entity.campaign_id.value,
            'timestamp': entity.timestamp.isoformat() if entity.timestamp else None
        }
