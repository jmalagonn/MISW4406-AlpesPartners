from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Date, String, Integer, DateTime, UUID, Text
import uuid

class Base(DeclarativeBase):
    pass

# Event Store Model (Write Side)
class EventModel(Base):
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False)
    event_type = Column(String(100), nullable=False)
    event_data = Column(Text, nullable=False)
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    event_metadata = Column(Text, nullable=True)

# Write Model (Write Side)
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

# Read Model (Read Side)
class InteractionReadModel(Base):
    __tablename__ = "interactions_read"
    __table_args__ = {'schema': 'read'}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interaction_type = Column(String(32), nullable=False)
    target_element_id = Column(String(255), nullable=False)
    target_element_type = Column(String(64), nullable=False)
    campaign_id = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)


class ConversionDailyStatus(Base):
    __tablename__ = "conversion_daily_status"
    day = Column(Date, primary_key=True)
    status = Column(String(32), primary_key=True)
    count = Column(Integer, nullable=False, default=0)

