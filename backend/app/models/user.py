from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class RoleEnum(str, Enum):
    ADMIN = "admin"
    ESTHETICIAN = "esthetician"
    RECEPTIONIST = "receptionist"
    PATIENT = "patient"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    appointments = relationship("Appointment", back_populates="provider", cascade="all,delete")
    reminders = relationship("ReminderLog", back_populates="user")
