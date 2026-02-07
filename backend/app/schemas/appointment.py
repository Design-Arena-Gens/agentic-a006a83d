from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    patient_id: int
    provider_id: int
    service_name: str
    start_time: datetime
    end_time: datetime
    status: str | None = None
    notes: str | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    service_name: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None
    notes: str | None = None
    provider_id: int | None = None


class AppointmentRead(AppointmentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
