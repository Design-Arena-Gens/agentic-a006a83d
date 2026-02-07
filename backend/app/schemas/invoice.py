from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InvoiceBase(BaseModel):
    appointment_id: int
    amount: float
    status: str | None = None
    stripe_payment_intent_id: str | None = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceRead(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
