from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReminderBase(BaseModel):
    appointment_id: int | None = None
    patient_id: int | None = None
    user_id: int | None = None
    channel: str
    message: str


class ReminderCreate(ReminderBase):
    pass


class ReminderRead(ReminderBase):
    id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
