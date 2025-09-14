from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Date, String, Integer

class Base(DeclarativeBase):
    pass

class ConversionDailyStatus(Base):
    __tablename__ = "conversion_daily_status"
    day = Column(Date, primary_key=True)
    status = Column(String(32), primary_key=True)
    count = Column(Integer, nullable=False, default=0)

