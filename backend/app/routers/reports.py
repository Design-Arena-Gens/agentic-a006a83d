from datetime import date, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import require_roles
from ..models import Appointment, Invoice, RoleEnum

router = APIRouter()


@router.get("/overview")
def overview(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN)),
):
    query_start = datetime.combine(start_date, datetime.min.time()) if start_date else None
    query_end = datetime.combine(end_date, datetime.max.time()) if end_date else None
    appointment_query = db.query(Appointment)
    invoice_query = db.query(Invoice)
    if query_start:
        appointment_query = appointment_query.filter(Appointment.start_time >= query_start)
        invoice_query = invoice_query.filter(Invoice.created_at >= query_start)
    if query_end:
        appointment_query = appointment_query.filter(Appointment.start_time <= query_end)
        invoice_query = invoice_query.filter(Invoice.created_at <= query_end)

    total_appointments = appointment_query.count()
    revenue = invoice_query.with_entities(func.sum(Invoice.amount)).scalar() or 0
    from ..models import InvoiceStatus

    paid_invoices = invoice_query.filter(Invoice.status == InvoiceStatus.PAID.value).count()
    return {
        "total_appointments": total_appointments,
        "total_revenue": float(revenue),
        "paid_invoices": paid_invoices,
    }
