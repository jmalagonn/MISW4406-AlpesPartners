from typing import override
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
        name = dto.name    
                    
        return Affiliate(name=name)    

    @override
    def entity_to_dto(self, entity: Entity) -> any:
        ...
        
class PostMapper(Mapper):
    @override
    def get_type(self) -> type:
        ...
        
    @override
    def dto_to_entity(self, dto: PostDTO) -> Post:
        title = dto.title
        content = dto.content
        affiliate_id = dto.affiliate_id
        brand_id = dto.brand_id
        
        return Post(title=title, content=content, affiliate_id=affiliate_id, brand_id=brand_id)

    @override
    def entity_to_dto(self, entity: Post) -> PostDTO:
        id = entity.id
        title = entity.title
        content = entity.content
        affiliate_id = entity.affiliate_id
        brand_id = entity.brand_id
        created_at = entity.created_at
        
        return PostDTO(
            id=id,
            title=title,
            content=content,
            affiliate_id=affiliate_id,
            brand_id=brand_id,
            created_at=created_at)
        