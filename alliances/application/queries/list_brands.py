from dataclasses import dataclass
from alliances.infrastructure.repository.brand_repository import BrandRepositoryDB


@dataclass
class ListBrands:
    limit: int = 50
    offset: int = 0
    

def handle_list_brands(q, session):
    repo = BrandRepositoryDB(session)
    rows = repo.get_all()
    
    return [
      {
        "id": c.id, 
        "name": c.name,
        "created_at": c.created_at.isoformat() if c.created_at else None
      } for c in rows
    ]
    
