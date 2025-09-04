from domain.models import Afiliate
from infrastructure.repository import AfiliateRepository

def handle_create_afiliate(cmd, session) -> str:
    repo = AfiliateRepository(session)    
    a = Afiliate(name=cmd.name.strip())
    repo.add(a)
    
    # Place to emit domain event "AfiliateCreated" via Outbox if needed
    return a.id

def handle_rename_afiliate(cmd, session):
    repo = AfiliateRepository(session)
    a = repo.get(cmd.afiliate_id)
    if not a:
        raise ValueError("Afiliate not found")
    a.rename(cmd.name)
