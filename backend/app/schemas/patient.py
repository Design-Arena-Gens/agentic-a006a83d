from datetime import date, datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class PatientBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    birth_date: date | None = None
    notes: str | None = None


class PatientCreate(PatientBase):
    user_id: int | None = None


class PatientUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birth_date: date | None = None
    notes: str | None = None


class PatientRead(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
