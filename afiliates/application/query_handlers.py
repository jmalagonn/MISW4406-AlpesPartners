from infrastructure.repository import AfiliateRepository

def handle_get_afiliate_by_id(q, session):
    repo = AfiliateRepository(session)
    c = repo.get(q.afiliate_id)
    if not c:
        return None
    return {
        "id": c.id,
        "name": c.name,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }

def handle_list_afiliates(q, session):
    repo = AfiliateRepository(session)
    rows = repo.list(limit=q.limit, offset=q.offset)
    return [
        {"id": c.id, "name": c.name,
         "created_at": c.created_at.isoformat() if c.created_at else None}
        for c in rows
    ]
