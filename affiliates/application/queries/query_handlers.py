from infrastructure.repository import AffiliateRepository

def handle_get_affiliate_by_id(q, session):
    repo = AffiliateRepository(session)
    c = repo.get(q.affiliate_id)
    if not c:
        return None
    return {
        "id": c.id,
        "name": c.name,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }

def handle_list_affiliates(q, session):
    repo = AffiliateRepository(session)
    rows = repo.list(limit=q.limit, offset=q.offset)
    return [
        {"id": c.id, "name": c.name,
         "created_at": c.created_at.isoformat() if c.created_at else None}
        for c in rows
    ]
