from dataclasses import dataclass
from datetime import datetime
from seedwork.application.dto import DTO


@dataclass(frozen=True)
class BrandDTO(DTO):
    id: str 
    name: str
    category: str
    created_at: str 
    updated_on: str

@dataclass(frozen=True)
class CreateBrandDTO(DTO):
    name: str
    category: str = "general"


@dataclass(frozen=True)
class CreatePaymentOrderDTO(DTO):
    post_id: str
    start_date: str
    end_date: str