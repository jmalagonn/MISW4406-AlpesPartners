from dataclasses import dataclass
from infrastructure.repository import AffiliateRepository

@dataclass
class RenameAffiliate:
    id: str
    name: str
    
  
def handle_rename_affiliate(cmd, session):
    repo = AffiliateRepository(session)
    a = repo.get(cmd.id)
    if not a:
        raise ValueError("Affiliate not found")
    a.rename(cmd.name)