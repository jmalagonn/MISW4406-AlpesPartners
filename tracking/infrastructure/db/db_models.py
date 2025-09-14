from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Date, String, Integer, DateTime, UUID
import uuid

class Base(DeclarativeBase):
    pass

class ConversionDailyStatus(Base):
    __tablename__ = "conversion_daily_status"
    day = Column(Date, primary_key=True)
    status = Column(String(32), primary_key=True)
    count = Column(Integer, nullable=False, default=0)


class InteractionModel(Base):
    __tablename__ = "interactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interaction_type = Column(String(32), nullable=False)
    target_element_id = Column(String(255), nullable=False)
    target_element_type = Column(String(64), nullable=False)
    campaign_id = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)

