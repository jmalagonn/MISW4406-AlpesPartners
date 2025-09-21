from datetime import datetime
from typing import override
import uuid
from affiliates.application.dto import AffiliateDTO, PostDTO
from affiliates.domain.entities import Affiliate, Post
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper


class AffiliateMapper(Mapper):
    @override
    def get_type(self) -> type:
        ...
        
    @override
    def dto_to_entity(self, dto: AffiliateDTO) -> Affiliate:
        return Affiliate(
            name=dto.name or "",
            email=dto.email or "",
            program_id=dto.program_id or uuid.uuid4(),
            status=dto.status or "pending",
            joined_at=dto.joined_at or datetime.now(),
        )

    @override
    def entity_to_dto(self, entity: Affiliate) -> AffiliateDTO:
        return AffiliateDTO(
            name=entity.name,
            email=entity.email,
            program_id=entity.program_id,
            status=entity.status,
            joined_at=entity.joined_at,
        )


class PostMapper(Mapper):
    @override
    def get_type(self) -> type:
        ...
        
    @override
    def dto_to_entity(self, dto: PostDTO) -> Post:
        return Post(
            title=dto.title or "",
            content=dto.content or "",
            affiliate_id=dto.affiliate_id or uuid.uuid4(),
            brand_id=dto.brand_id or uuid.uuid4(),
        )

    @override
    def entity_to_dto(self, entity: Post) -> PostDTO:
        return PostDTO(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            affiliate_id=entity.affiliate_id,
            brand_id=entity.brand_id,
            created_at=entity.created_at,
        )