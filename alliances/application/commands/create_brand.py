import logging
from dataclasses import dataclass, asdict
from typing import override
from alliances.application.dto.dto import CreateBrandDTO
from alliances.application.mappers.brand_mapper import BrandMapper
from alliances.domain.factories.brand_factory import BrandFactory
from alliances.domain.repositories import BrandRepository
from alliances.domain.entities import Brand
from alliances.infrastructure.factories.brand_factory import RepositoryFactory
from seedwork.application.commands import Command, CommandHandler

@dataclass
class CreateBrand(Command):
    name: str
    category: str = "general"


class CreateBrandHandler(CommandHandler):
    def __init__(self, session):
        self.session = session
        self.repository_factory: RepositoryFactory = RepositoryFactory(session=session)
        self.brand_factory: BrandFactory = BrandFactory()
        
    @override
    def handle(self, command: CreateBrand):
        logging.info("Received command=%s", asdict(command))
        
        brand_dto = CreateBrandDTO(name=command.name, category=command.category)
        
        repo: BrandRepository = self.repository_factory.create_object(BrandRepository)
        brand: Brand = self.brand_factory.create_object(brand_dto, BrandMapper())
        
        repo.add(brand)
        self.session.commit()
        logging.info("Brand created with id=%s", brand.id)