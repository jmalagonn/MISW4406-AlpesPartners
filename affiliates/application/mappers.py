from typing import override
from affiliates.application.dto import AffiliateDTO
from affiliates.domain.models import Affiliate
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper


class AffiliateMapper(Mapper):
    @override
    def get_type(self) -> type:
        ...
        
    @override
    def dto_to_entity(self, dto: AffiliateDTO) -> Affiliate:
        name = dto.name                
        affiliate = Affiliate(name=name)
        
        return affiliate      

    @override
    def entity_to_dto(self, entity: Entity) -> any:
        ...