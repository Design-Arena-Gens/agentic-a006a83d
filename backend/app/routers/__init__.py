from fastapi import APIRouter

from . import appointments, auth, inventory, patients, reminders, reports, billing

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
