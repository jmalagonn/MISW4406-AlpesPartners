from abc import ABC, abstractmethod
from .entities import Entity

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