from domain.value_objects import Name
from domain.models import Affiliate
from infrastructure.repository import AffiliateRepository

def handle_create_affiliate(cmd, session) -> str:
    repo = AffiliateRepository(session)   
    a = Affiliate(name=Name((cmd.name or "").strip()))
    repo.add(a)
        
    return a.id

def handle_rename_affiliate(cmd, session):
    repo = AffiliateRepository(session)
    a = repo.get(cmd.id)
    if not a:
        raise ValueError("Affiliate not found")
    a.rename(cmd.name)
