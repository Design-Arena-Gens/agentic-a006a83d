from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from ..models.user import RoleEnum


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
