from pydantic import BaseModel, ConfigDict
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    password: str


class CreateUserRequest(BaseModel):
    nama: str
    username: str
    role: str
    pelanggan_id: Optional[int] = None
    aktif: Optional[bool] = True
    force_password_change: Optional[bool] = True

class ProfileUpdateRequest(BaseModel):
    nama: str
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nama: str
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nama: str
    username: str
    role: str
    pelanggan_id: Optional[int] = None
    aktif: bool
