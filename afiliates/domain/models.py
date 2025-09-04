from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
import uuid

class Base(DeclarativeBase):
    pass

class Afiliate(Base):
    __tablename__ = "afiliates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def rename(self, new_name: str):
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("Afiliate name too short")
        self.name = new_name.strip()
