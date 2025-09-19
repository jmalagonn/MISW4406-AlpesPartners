from dataclasses import dataclass
from affiliates.domain.models import Affiliate, Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper


@dataclass
class AffiliateFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        else:
            affiliate: Affiliate = mapper.dto_to_entity(obj)
            
            return affiliate  