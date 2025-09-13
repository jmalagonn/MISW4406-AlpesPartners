from dataclasses import dataclass
from domain.models import Affiliate
from domain.value_objects import Name
from infrastructure.repository import AffiliateRepository


@dataclass
class CreateAffiliate:
    name: str
    
    
def handle_create_affiliate(cmd, session) -> str:
    repo = AffiliateRepository(session)   
    a = Affiliate(name=Name((cmd.name or "").strip()))
    repo.add(a)
        
    return a.id