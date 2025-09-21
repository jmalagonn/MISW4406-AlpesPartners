from dataclasses import dataclass
from alliances.infrastructure.repository.brand_repository import BrandRepositoryDB


@dataclass
class ListBrands:
    ...
    

def handle_list_brands(session):
    repo = BrandRepositoryDB(session)
    rows = repo.get_all()
    
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "category": c.category,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_on": c.updated_on.isoformat() if c.updated_on else None
        }
        for c in rows
    ]