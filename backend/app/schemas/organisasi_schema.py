from pydantic import BaseModel
from typing import Optional


# =========================
# CREATE / UPDATE
# =========================
class OrganisasiCreate(BaseModel):
    pelanggan_id: int
    kod: str
    nama: str
    keterangan: Optional[str] = None
    pegawai_tadbir: Optional[str] = None   # ✅ ADD
    jawatan: Optional[str] = None          # ✅ ADD


# =========================
# RESPONSE
# =========================
class OrganisasiResponse(BaseModel):
    id: int
    pelanggan_id: int
    kod: str
    nama: str
    keterangan: Optional[str]
    pegawai_tadbir: Optional[str] = None   # ✅ ADD
    jawatan: Optional[str] = None          # ✅ ADD
    aktif: bool
    sub_count: int = 0
    tapak_count: int = 0
    class Config:
        from_attributes = True