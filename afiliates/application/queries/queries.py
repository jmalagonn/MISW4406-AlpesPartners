from dataclasses import dataclass

@dataclass
class GetAfiliateById:
    afiliate_id: str

@dataclass
class ListAfiliates:
    limit: int = 50
    offset: int = 0
