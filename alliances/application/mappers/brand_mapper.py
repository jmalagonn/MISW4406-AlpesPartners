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
        brand = Brand(
            name=dto.name,
            category=getattr(dto, "category", "general")
        )
        return brand

    @override
    def entity_to_dto(self, entity: Brand) -> BrandDTO:
        return BrandDTO(
            id=entity.id,
            name=entity.name,
            category=getattr(entity, "category", "general"),
            created_at=entity.created_at,
            updated_on=entity.updated_on
        )