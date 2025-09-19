from dataclasses import dataclass
from seedwork.application.dto import DTO


@dataclass(frozen=True)
class AffiliateDTO(DTO):
    name: str