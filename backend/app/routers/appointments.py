from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user, require_roles
from ..models import Appointment, RoleEnum, User
from ..schemas import AppointmentCreate, AppointmentRead, AppointmentUpdate
from ..services.calendar import CalendarService

router = APIRouter()


def _validate_conflict(db: Session, payload: AppointmentCreate, appointment_id: int | None = None) -> None:
    conflict = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == payload.provider_id,
            or_(
                and_(Appointment.start_time <= payload.start_time, Appointment.end_time > payload.start_time),
                and_(Appointment.start_time < payload.end_time, Appointment.end_time >= payload.end_time),
                and_(Appointment.start_time >= payload.start_time, Appointment.end_time <= payload.end_time),
            ),
        )
    )
    if appointment_id:
        conflict = conflict.filter(Appointment.id != appointment_id)
    if conflict.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflito de horário detectado")


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Appointment)
    if current_user.role == RoleEnum.ESTHETICIAN:
        query = query.filter(Appointment.provider_id == current_user.id)
    return query.order_by(Appointment.start_time).all()


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    _validate_conflict(db, payload)
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    CalendarService(db).sync_appointment(appointment)
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")
    if payload.start_time or payload.end_time:
        merged = AppointmentCreate(
            patient_id=appointment.patient_id,
            provider_id=payload.provider_id or appointment.provider_id,
            service_name=payload.service_name or appointment.service_name,
            start_time=payload.start_time or appointment.start_time,
            end_time=payload.end_time or appointment.end_time,
            status=payload.status or appointment.status,
            notes=payload.notes or appointment.notes,
        )
        _validate_conflict(db, merged, appointment_id=appointment.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(appointment, key, value)
    db.commit()
    db.refresh(appointment)
    CalendarService(db).sync_appointment(appointment)
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST)),
):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")
    CalendarService(db).delete_event(appointment)
    db.delete(appointment)
    db.commit()
