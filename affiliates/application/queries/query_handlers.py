from affiliates.infrastructure.repository.affiliate_repository import AffiliateRepositoryDB


def handle_list_affiliates(session):
    repo = AffiliateRepositoryDB(session)
    rows = repo.get_all() 
    
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "email": str(c.email),
            "program_id": str(c.program_id),
            "status": c.status,
            "joined_at": c.joined_at.isoformat() if c.joined_at else None,
            "updated_on": c.updated_on.isoformat() if c.updated_on else None,
            "created_at" : c.created_at.isoformat() if c.created_at else None
        }
        for c in rows
    ]