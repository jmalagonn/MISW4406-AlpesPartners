from afiliates.presentation.worker import publish_afiliate_created_event
from domain.models import Afiliate
from infrastructure.repository import AfiliateRepository

def handle_create_afiliate(cmd, session) -> str:
    repo = AfiliateRepository(session)    
    a = Afiliate(name=cmd.name.strip())
    repo.add(a)
    
    for event in a.events:
        publish_afiliate_created_event.delay({
            "afiliate_id": event.afiliate_id,
            "name": event.name,
            "created_at": event.created_at.isoformat()
        })
        
    return a.id

def handle_rename_afiliate(cmd, session):
    repo = AfiliateRepository(session)
    a = repo.get(cmd.afiliate_id)
    if not a:
        raise ValueError("Afiliate not found")
    a.rename(cmd.name)
