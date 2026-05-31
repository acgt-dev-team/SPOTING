from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    nama: str
    username: str
    role: str
    pelanggan_id: Optional[int] = None
    aktif: Optional[bool] = True
    force_password_change: Optional[bool] = True