from abc import ABC, abstractmethod
from typing import Any

class Projection(ABC):
    """
    Interfaz base para todas las proyecciones
    """
    
    @abstractmethod
    def handle_event(self, event: Any) -> None:
        """
        Procesa un evento de dominio y actualiza la proyección
        """
        pass
    
    @abstractmethod
    def get_projection_name(self) -> str:
        """
        Retorna el nombre de la proyección
        """
        pass
