from dataclasses import dataclass
from seedwork.application.dto import DTO


@dataclass(frozen=True)
class CreatePaymentOrderDTO(DTO):
    start_date: str
    end_date: str
    post_id: str