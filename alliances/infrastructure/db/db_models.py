from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
import uuid
from datetime import datetime

class Base(DeclarativeBase):
    pass