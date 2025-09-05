from .rules import BusinessRule

class DomainException(Exception):
  ...


class IdMustBeImmutableException(DomainException):
  def __init__(self, message='The identifier must be immutable'):
    self.__message = message
  def __str__(self):
    return str(self.__message)