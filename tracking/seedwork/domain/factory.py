from abc import ABC, abstractmethod
from typing import Any


class Factory(ABC):
    """
    Clase base para todas las factories del dominio
    """
    
    @abstractmethod
    def create_object(self, obj: Any, mapper: Any = None) -> Any:
        """
        Método abstracto que debe implementar cada factory específica
        """
        pass
    
    def validate_rule(self, rule):
        """
        Valida una regla de negocio y lanza excepción si no es válida
        """
        if not rule.is_valid():
            raise ValueError(rule.error_message())
