from pydantic import BaseModel


class SubOrganisasiCreate(BaseModel):
    organisasi_id: int
    kod: str
    nama: str
    keterangan: str | None = None


class SubOrganisasiResponse(BaseModel):
    id: int
    organisasi_id: int
    kod: str
    nama: str
    keterangan: str | None
    aktif: bool

    class Config:
        from_attributes = True