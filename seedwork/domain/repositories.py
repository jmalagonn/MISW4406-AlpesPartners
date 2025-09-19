from abc import ABC, abstractmethod
from uuid import UUID
from .entities import Entity

class Repository(ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Entity:
        ...

    @abstractmethod
    def get_all(self) -> list[Entity]:
        ...

    @abstractmethod
    def add(self, entity: Entity):
        ...

    @abstractmethod
    def update(self, entity: Entity):
        ...

    @abstractmethod
    def delete(self, entity_id: UUID):
        ...
        

class Mapper(ABC):
    @abstractmethod
    def get_type(self) -> type:
        ...

    @abstractmethod
    def entity_to_dto(self, entity: Entity) -> any:
        ...

    @abstractmethod
    def dto_to_entity(self, dto: any) -> Entity:
        ...