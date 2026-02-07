from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger
from sqlalchemy.orm import Session

from ..config import get_settings
from ..models import Appointment


class CalendarService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        self._client = None

    def _get_credentials(self):
        if not self.settings.GOOGLE_SERVICE_ACCOUNT_FILE:
            return None
        file_path = Path(self.settings.GOOGLE_SERVICE_ACCOUNT_FILE)
        if not file_path.exists():
            logger.warning("Google service account file not found: {}", file_path)
            return None
        return service_account.Credentials.from_service_account_file(
            str(file_path),
            scopes=["https://www.googleapis.com/auth/calendar"],
        )

    def _get_calendar_client(self):
        if self._client:
            return self._client
        credentials = self._get_credentials()
        if not credentials:
            return None
        self._client = build("calendar", "v3", credentials=credentials, cache_discovery=False)
        return self._client

    def sync_appointment(self, appointment: Appointment) -> None:
        client = self._get_calendar_client()
        if not client:
            return
        body: dict[str, Any] = {
            "summary": f"{appointment.service_name} - Paciente #{appointment.patient_id}",
            "start": {"dateTime": appointment.start_time.isoformat()},
            "end": {"dateTime": appointment.end_time.isoformat()},
            "description": appointment.notes or "",
        }
        try:
            client.events().insert(calendarId="primary", body=body).execute()
        except HttpError as exc:
            logger.error("Failed to sync appointment {}: {}", appointment.id, exc)

    def delete_event(self, appointment: Appointment) -> None:
        client = self._get_calendar_client()
        if not client:
            return
        try:
            client.events().delete(calendarId="primary", eventId=str(appointment.id)).execute()
        except HttpError as exc:
            logger.warning("Failed to delete calendar event {}: {}", appointment.id, exc)
