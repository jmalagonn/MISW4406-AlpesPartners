import logging
from dataclasses import asdict, dataclass
from typing import override
from uuid import UUID

from affiliates.application.dto import AffiliateDTO
from affiliates.application.mappers import AffiliateMapper
from affiliates.domain.factories import AffiliateFactory
from affiliates.infrastructure.factories import RepositoryFactory
from affiliates.domain.entities import Affiliate
from affiliates.infrastructure.repository.affiliate_repository import AffiliateRepository
from seedwork.application.commands import CommandHandler


@dataclass
class CreateAffiliate:
    name: str
    email: str
    program_id: UUID   # obligatorio en el nuevo dominio


class CreateAffiliateHandler(CommandHandler):
    def __init__(self, session):
        self.session = session
        self.repository_factory: RepositoryFactory = RepositoryFactory(session=session)
        self.affiliate_factory: AffiliateFactory = AffiliateFactory()

    @override
    def handle(self, command: CreateAffiliate):
        logging.info("Received command=%s", asdict(command))

        # Ahora el DTO debe incluir los nuevos campos
        affiliate_dto = AffiliateDTO(
            name=command.name,
            email=command.email,
            program_id=command.program_id,
            status="pending"  # inicial por defecto
        )

        repo: AffiliateRepository = self.repository_factory.create_object(AffiliateRepository)
        affiliate: Affiliate = self.affiliate_factory.create_object(affiliate_dto, AffiliateMapper())

        repo.add(affiliate)
        self.session.commit()

        logging.info("Affiliate created with id=%s", affiliate.id)