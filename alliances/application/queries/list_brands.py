from dataclasses import dataclass
from infrastructure.repository.brand_repository import BrandRepository


@dataclass
class ListBrands:
    limit: int = 50
    offset: int = 0
    

def handle_list_brands(q, session):
    repo = BrandRepository(session)
    rows = repo.list(limit=q.limit, offset=q.offset)
    
    return [
      {
        "id": c.id, 
        "name": c.name,
        "created_at": c.created_at.isoformat() if c.created_at else None
      } for c in rows
    ]
    
