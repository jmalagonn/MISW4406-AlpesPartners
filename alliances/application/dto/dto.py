from dataclasses import dataclass
from seedwork.application.dto import DTO


@dataclass(frozen=True)
class BrandDTO(DTO):
    name: str


@dataclass(frozen=True)
class CreatePaymentOrderDTO(DTO):
    post_id: str
    start_date: str
    end_date: str