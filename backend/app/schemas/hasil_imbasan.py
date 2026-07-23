from uuid import UUID

from pydantic import BaseModel
from typing import Any


class HasilImbasanCreate(BaseModel):
    profil_tugasan_id: int
    ejen_id: int
    machine_id: UUID
    hasil: Any


class HasilImbasanResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True