from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from seedwork.application.dto import DTO
from datetime import datetime

@dataclass(frozen=True)
class AffiliateDTO(DTO):
    name: str
    email: str
    program_id: UUID
    status: str = "pending"
    joined_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    
@dataclass(frozen=True)
class PostDTO(DTO):
    id: str
    title: str
    content: str
    affiliate_id: str
    brand_id: str
    created_at: Optional[str] = None