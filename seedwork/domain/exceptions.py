from .rules import BusinessRule

class DomainException(Exception):
    ...


class BusinessRuleException(DomainException):
    def __init__(self, rule: BusinessRule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
    

class IdMustBeImmutableException(DomainException):
    def __init__(self, message='The id of an entity must be immutable'):
        self.__message = message
    def __str__(self):
        return str(self.__message)
    
    
class FactoryException(DomainException):
    def __init__(self, message):
        self.__message = message
    def __str__(self):
        return str(self.__message)