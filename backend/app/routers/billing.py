from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import require_roles
from ..models import Appointment, Invoice, InvoiceStatus, RoleEnum
from ..schemas import InvoiceCreate, InvoiceRead
from ..services import PaymentService

router = APIRouter()


@router.get("/", response_model=list[InvoiceRead])
def list_invoices(
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST)),
):
    return db.query(Invoice).all()


@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST)),
):
    appointment = db.get(Appointment, payload.appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")
    invoice = Invoice(**payload.model_dump())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    PaymentService(db).create_payment_intent(invoice)
    return invoice


@router.post("/{invoice_id}/capture", response_model=InvoiceRead)
def capture_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN)),
):
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fatura inexistente")
    invoice.status = InvoiceStatus.PAID.value
    db.commit()
    db.refresh(invoice)
    return invoice
