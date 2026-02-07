from loguru import logger
from sqlalchemy.orm import Session
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from ..config import get_settings
from ..models import Appointment, ReminderLog


class ReminderService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        self.client = None
        if self.settings.TWILIO_ACCOUNT_SID and self.settings.TWILIO_AUTH_TOKEN:
            self.client = Client(self.settings.TWILIO_ACCOUNT_SID, self.settings.TWILIO_AUTH_TOKEN)

    def send_sms(self, to_number: str, message: str, appointment: Appointment | None = None) -> ReminderLog:
        status = "queued"
        if self.client:
            try:
                response = self.client.messages.create(
                    body=message, from_=self.settings.TWILIO_FROM_NUMBER, to=to_number
                )
                status = response.status or "sent"
            except TwilioRestException as exc:
                logger.error("Failed to send SMS reminder: {}", exc)
                status = "failed"
        else:
            logger.info("Twilio disabled. Logging reminder for {}", to_number)
        reminder = ReminderLog(
            patient_id=getattr(appointment, "patient_id", None) if appointment else None,
            appointment_id=getattr(appointment, "id", None) if appointment else None,
            channel="sms",
            status=status,
            message=message,
        )
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder
