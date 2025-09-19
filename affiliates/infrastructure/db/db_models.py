from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Base(DeclarativeBase):
    pass

class AffiliateDBModel(Base):
    __tablename__ = "affiliates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)