import json, logging
from domain.value_objects import Name
from domain.models import Brand
from infrastructure.db.brand_repository import BrandRepository


def handle_create_brand(cmd, session) -> str: 
  logging.info("Received command=%s", json.dumps(cmd))
  
  repo = BrandRepository(session)
  brand = Brand(name=Name(cmd.name))
  repo.add(brand)
  
  return brand.id