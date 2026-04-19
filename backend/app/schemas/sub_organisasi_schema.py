from pydantic import BaseModel
from typing import Optional


class SubOrganisasiCreate(BaseModel):
    organisasi_id: int
    kod: str
    nama: str
    keterangan: Optional[str] = None
    pegawai_tadbir: Optional[str] = None   # ✅ ADD
    jawatan: Optional[str] = None          # ✅ ADD


class SubOrganisasiResponse(BaseModel):
    id: int
    organisasi_id: int
    kod: str
    nama: str
    keterangan: Optional[str]
    pegawai_tadbir: Optional[str] = None   # ✅ ADD
    jawatan: Optional[str] = None          # ✅ ADD
    aktif: bool

    class Config:
        from_attributes = True