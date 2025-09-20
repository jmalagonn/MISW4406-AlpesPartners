from dataclasses import dataclass
from typing import Optional
from seedwork.application.dto import DTO


@dataclass(frozen=True)
class AffiliateDTO(DTO):
    name: str
    
    
@dataclass(frozen=True)
class PostDTO(DTO):
    id: str
    title: str
    content: str
    affiliate_id: str
    brand_id: str
    created_at: Optional[str] = None