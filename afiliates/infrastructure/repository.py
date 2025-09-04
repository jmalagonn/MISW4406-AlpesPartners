from typing import Optional, List
from sqlalchemy import select
from domain.models import Afiliate

class AfiliateRepository:
    def __init__(self, session):
        self.session = session

    def add(self, afiliate: Afiliate):
        self.session.add(afiliate)

    def get(self, afiliate_id: str) -> Optional[Afiliate]:
        return self.session.get(Afiliate, afiliate_id)

    def list(self, limit: int = 50, offset: int = 0) -> List[Afiliate]:
        stmt = select(Afiliate).order_by(Afiliate.created_at.desc()).limit(limit).offset(offset)
        return list(self.session.execute(stmt).scalars())
