from abc import ABC, abstractmethod


class BusinessRule(ABC):

  __message: str = 'The business rule is invalid'

  def __init__(self, message):
    self.__message = message

  def error_message(self) -> str:
    return self.__message

  @abstractmethod
  def is_valid(self) -> bool:
    ...

  def __str__(self):
    return f"{self.__class__.__name__} - {self.__message}"
  

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
