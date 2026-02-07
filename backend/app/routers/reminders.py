from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import require_roles
from ..models import Appointment, ReminderLog, RoleEnum
from ..schemas import ReminderCreate, ReminderRead
from ..services import ReminderService

router = APIRouter()


@router.get("/", response_model=list[ReminderRead])
def list_reminders(
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST)),
):
    return db.query(ReminderLog).order_by(ReminderLog.created_at.desc()).all()


@router.post("/", response_model=ReminderRead, status_code=status.HTTP_201_CREATED)
def send_reminder(
    payload: ReminderCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    appointment = None
    if payload.appointment_id:
        appointment = db.get(Appointment, payload.appointment_id)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")
    service = ReminderService(db)
    reminder = service.send_sms(
        to_number=payload.message.split("|")[0] if "|" in payload.message else "+5511999999999",
        message=payload.message,
        appointment=appointment,
    )
    return reminder
