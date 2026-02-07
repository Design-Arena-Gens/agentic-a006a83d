import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test.db")
os.environ.setdefault("ALLOWED_ORIGINS", "[]")

from app.main import app  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import User, RoleEnum  # noqa: E402
from app.core.security import get_password_hash  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_client(db: Session) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def admin_user(db: Session) -> User:
    existing = db.query(User).filter(User.email == "admin@example.com").first()
    if existing:
        return existing
    user = User(
        email="admin@example.com",
        full_name="Admin",
        role=RoleEnum.ADMIN,
        hashed_password=get_password_hash("secret"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
