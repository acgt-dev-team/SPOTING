from pydantic import BaseModel
from uuid import UUID


class EjenRegister(BaseModel):
    ip_address: str
    tapak_id: int
    profile_id: int
    machine_id: UUID
    hostname: str
    


class EjenResponse(BaseModel):
    id: int
    ip_address: str
    machine_id: UUID
    hostname: str
    profile_id: int

    class Config:
        from_attributes = True
