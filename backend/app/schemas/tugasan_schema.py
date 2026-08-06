from pydantic import BaseModel, Field
from typing import Optional
from app.i18n import t


# =========================
# CREATE SCHEMA
# =========================
class TugasanCreate(BaseModel):
    nama: str = Field(..., example=t("docs.examples.taskName"))
    kod: str = Field(..., example="TSK001")
    keterangan: Optional[str] = Field(None, example=t("docs.examples.taskDescription"))
    jenis_id: int = Field(..., example=1)

    # ✅ ADD THESE
    protocol: Optional[str] = Field(None, example="TCP")
    ip_start: Optional[str] = Field(None, example="192.168.1.1")
    ip_end: Optional[str] = Field(None, example="192.168.1.255")

    aktif: Optional[bool] = True


# =========================
# RESPONSE SCHEMA
# =========================
class TugasanResponse(BaseModel):
    id: int
    nama: str
    kod: str
    keterangan: Optional[str]
    jenis_id: int

    protocol: Optional[str]
    ip_start: Optional[str]
    ip_end: Optional[str]

    aktif: bool

    # New fields
    status: int

    agent_count: int = 0
    completed_agent_count: int = 0

    class Config:
        from_attributes = True
