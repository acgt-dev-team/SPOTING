from pydantic import BaseModel
from typing import Optional


class EjenRegister(BaseModel):
    ip_address: str
    tapak_id: int
    tugasan_id: Optional[int] = None


class EjenResponse(BaseModel):
    id: int
    ip_address: str

    class Config:
        from_attributes = True