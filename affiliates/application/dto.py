from dataclasses import dataclass
from seedwork.application.dto import DTO


@dataclass(frozen=True)
class AffiliateDTO(DTO):
    name: str
    
    
@dataclass(frozen=True)
class PostDTO(DTO):
    title: str
    content: str
    affiliate_id: str
    brand_id: str