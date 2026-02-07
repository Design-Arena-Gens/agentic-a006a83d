from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models import Appointment, Patient, RoleEnum, User


def authenticate(user: User):
    token = create_access_token(str(user.id))
    return {"Authorization": f"Bearer {token}"}


def create_patient(db: Session) -> Patient:
    patient = Patient(full_name="Paciente Teste", email="p@example.com", phone="+5511999999999")
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def test_create_appointment_success(test_client: TestClient, db: Session, admin_user: User):
    patient = create_patient(db)
    payload = {
        "patient_id": patient.id,
        "provider_id": admin_user.id,
        "service_name": "Limpeza de pele",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }
    response = test_client.post(
        "/api/v1/appointments/", json=payload, headers=authenticate(admin_user)
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["patient_id"] == patient.id
    assert data["provider_id"] == admin_user.id


def test_create_appointment_conflict(test_client: TestClient, db: Session, admin_user: User):
    patient = create_patient(db)
    start_time = datetime.utcnow()
    appointment = Appointment(
        patient_id=patient.id,
        provider_id=admin_user.id,
        service_name="Tratamento A",
        start_time=start_time,
        end_time=start_time + timedelta(hours=1),
    )
    db.add(appointment)
    db.commit()
    payload = {
        "patient_id": patient.id,
        "provider_id": admin_user.id,
        "service_name": "Tratamento B",
        "start_time": (start_time + timedelta(minutes=30)).isoformat(),
        "end_time": (start_time + timedelta(hours=1, minutes=30)).isoformat(),
    }
    response = test_client.post(
        "/api/v1/appointments/", json=payload, headers=authenticate(admin_user)
    )
    assert response.status_code == 409
