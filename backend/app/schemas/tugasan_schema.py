from pydantic import BaseModel, Field
from typing import Optional


# =========================
# CREATE SCHEMA
# =========================
class TugasanCreate(BaseModel):
    nama: str = Field(..., example="Port Scan")
    kod: str = Field(..., example="TSK001")
    keterangan: Optional[str] = Field(None, example="Scan open ports")
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

    # ✅ ADD THESE (important for frontend display)
    protocol: Optional[str]
    ip_start: Optional[str]
    ip_end: Optional[str]

    aktif: bool

    class Config:
        from_attributes = True