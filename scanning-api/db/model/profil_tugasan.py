from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel

class ProfilTugasan(SQLModel, table=True):
    __tablename__ = 'x_profil_tugasan'

    id: int = Field(primary_key=True)
    jadualkan_pada: datetime | None
    selesai_pada: datetime | None
    tugasan_id: int = Field(foreign_key='tugasan.id')
    status_id: int = Field(foreign_key='status.id')

class ProfilTugasanEjenResponse(BaseModel):
    jadualkan_pada: datetime | None