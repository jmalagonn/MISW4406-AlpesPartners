import logging
from dataclasses import dataclass, asdict
from domain.value_objects import Name
from domain.models import Brand
from infrastructure.repository.brand_repository import BrandRepository

@dataclass
class CreateBrand:
    name: str
    

def handle_create_brand(cmd: CreateBrand, session) -> str: 
  logging.info("Received command=%s", asdict(cmd))
  
  brand = Brand(name=Name(cmd.name))
  
  repo = BrandRepository(session)
  repo.add(brand)
  
  return brand.id