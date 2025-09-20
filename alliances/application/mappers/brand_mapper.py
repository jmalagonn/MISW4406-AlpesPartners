from typing import override
from alliances.application.dto.dto import BrandDTO
from alliances.domain.entities import Brand
from alliances.domain.value_objects import Name
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper


class BrandMapper(Mapper):
    @override
    def get_type(self) -> type:
        ...
        
    @override
    def dto_to_entity(self, dto: BrandDTO) -> Brand:
        name = dto.name                
        brand = Brand(name=name)
        
        return brand      

    @override
    def entity_to_dto(self, entity: Entity) -> any:
        ...