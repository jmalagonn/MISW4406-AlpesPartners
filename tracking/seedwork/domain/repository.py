from abc import ABC, abstractmethod
from typing import List, Any, Optional


class Repository(ABC):
    """
    Interfaz base para todos los repositorios
    """
    
    @abstractmethod
    def add(self, entity: Any) -> None:
        """
        Agrega una entidad al repositorio
        """
        pass
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Any]:
        """
        Obtiene una entidad por su ID
        """
        pass
    
    @abstractmethod
    def list(self, limit: int = 50, offset: int = 0) -> List[Any]:
        """
        Lista entidades con paginación
        """
        pass
    
    @abstractmethod
    def update(self, entity: Any) -> None:
        """
        Actualiza una entidad existente
        """
        pass
    
    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Elimina una entidad por su ID
        """
        pass


class Mapper(ABC):
    """
    Interfaz base para todos los mapeadores
    """
    
    @abstractmethod
    def dto_to_entity(self, dto: Any) -> Any:
        """
        Convierte un DTO a entidad
        """
        pass
    
    @abstractmethod
    def entity_to_dto(self, entity: Any) -> Any:
        """
        Convierte una entidad a DTO
        """
        pass
