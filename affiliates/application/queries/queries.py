from dataclasses import dataclass

@dataclass
class GetAffiliateById:
    affiliate_id: str

@dataclass
class ListAffiliates:
    limit: int = 50
    offset: int = 0
