from affiliates.infrastructure.repository.affiliate_repository import AffiliateRepositoryDB


def handle_list_affiliates(session):
    repo = AffiliateRepositoryDB(session)
    rows = repo.get_all()
    
    return [
        {"id": c.id, "name": c.name, "created_at": c.created_at.isoformat() if c.created_at else None}
        for c in rows
    ]
