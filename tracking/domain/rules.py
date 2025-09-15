from seedwork.domain.rules import BusinessRule
  

class IdentityIdIsInmutable(BusinessRule):
  entity: object

  def __init__(self, entity, message='The entity identifier must be immutable'):
    super().__init__(message)
    self.entity = entity

  def is_valid(self) -> bool:
    try:
      if self.entity._id:
        return False
    except AttributeError:
      return True


class InteractionTrackingRules:
    @staticmethod
    def is_valid_interaction_type(interaction_type: str) -> bool:
        valid_types = ['click', 'view', 'like']
        return interaction_type in valid_types
    
    @staticmethod
    def is_valid_target_element(element_id: str, element_type: str) -> bool:
        return (
            element_id and len(element_id.strip()) > 0 and
            element_type and len(element_type.strip()) > 0
        )
    
    @staticmethod
    def is_valid_campaign_id(campaign_id: str) -> bool:
        return campaign_id and len(campaign_id.strip()) > 0


# Reglas específicas para Interaction
class InteractionTypeCannotBeEmpty(BusinessRule):
    """
    Regla: El tipo de interacción no puede estar vacío
    """
    interaction_type: str
    
    def __init__(self, interaction_type: str, message='Interaction type cannot be empty'):
        super().__init__(message)
        self.interaction_type = interaction_type
    
    def is_valid(self) -> bool:
        return self.interaction_type and len(self.interaction_type.strip()) > 0


class InteractionTypeMustBeValid(BusinessRule):
    """
    Regla: El tipo de interacción debe ser válido
    """
    interaction_type: str
    
    def __init__(self, interaction_type: str, message='Invalid interaction type'):
        super().__init__(message)
        self.interaction_type = interaction_type
    
    def is_valid(self) -> bool:
        valid_types = ['click', 'view', 'like']
        return self.interaction_type in valid_types


class TargetElementIdCannotBeEmpty(BusinessRule):
    """
    Regla: El ID del elemento objetivo no puede estar vacío
    """
    element_id: str
    
    def __init__(self, element_id: str, message='Target element ID cannot be empty'):
        super().__init__(message)
        self.element_id = element_id
    
    def is_valid(self) -> bool:
        return self.element_id and len(self.element_id.strip()) > 0


class TargetElementTypeCannotBeEmpty(BusinessRule):
    """
    Regla: El tipo del elemento objetivo no puede estar vacío
    """
    element_type: str
    
    def __init__(self, element_type: str, message='Target element type cannot be empty'):
        super().__init__(message)
        self.element_type = element_type
    
    def is_valid(self) -> bool:
        return self.element_type and len(self.element_type.strip()) > 0


class CampaignIdCannotBeEmpty(BusinessRule):
    """
    Regla: El ID de campaña no puede estar vacío
    """
    campaign_id: str
    
    def __init__(self, campaign_id: str, message='Campaign ID cannot be empty'):
        super().__init__(message)
        self.campaign_id = campaign_id
    
    def is_valid(self) -> bool:
        return self.campaign_id and len(self.campaign_id.strip()) > 0