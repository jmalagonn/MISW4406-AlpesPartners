from abc import ABC, abstractmethod


class BusinessRule(ABC):
    """
    Clase base para todas las reglas de negocio
    """
    
    __message: str = 'The business rule is invalid'

    def __init__(self, message: str = None):
        if message:
            self.__message = message

    def error_message(self) -> str:
        return self.__message

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Método abstracto que debe implementar cada regla específica
        """
        pass

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__message}"
