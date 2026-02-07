from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, require_roles
from ..models import Patient, RoleEnum
from ..schemas import PatientCreate, PatientRead, PatientUpdate
from ..database import get_db

router = APIRouter()


@router.get("/", response_model=list[PatientRead])
def list_patients(
    db: Session = Depends(get_db), _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST))
):
    return db.query(Patient).all()


@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    return patient


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN)),
):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    db.delete(patient)
    db.commit()
