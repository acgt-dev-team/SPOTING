from pydantic import BaseModel


class OrganisasiCreate(BaseModel):
    pelanggan_id: int
    kod: str
    nama: str
    keterangan: str | None = None


class OrganisasiResponse(BaseModel):
    id: int
    nama: str
    keterangan: str | None
    kod: str
    aktif: bool

    class Config:
        from_attributes = True