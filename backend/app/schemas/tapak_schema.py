from pydantic import BaseModel
from typing import Optional


class TapakCreate(BaseModel):
    sub_organisasi_id: int
    nama: str
    keterangan: Optional[str] = None
    pegawai_tadbir: Optional[str] = None   # ✅ ADD
    jawatan: Optional[str] = None          # ✅ ADD


class TapakResponse(BaseModel):
    id: int
    sub_organisasi_id: int
    kod: str
    nama: str
    keterangan: Optional[str]
    pegawai_tadbir: Optional[str] = None   # ✅ ADD
    jawatan: Optional[str] = None          # ✅ ADD
    aktif: bool
    tugasan_count: int = 0

    class Config:
        from_attributes = True