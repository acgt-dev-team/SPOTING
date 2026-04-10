from pydantic import BaseModel


class ProfilCreate(BaseModel):
    tapak_id: int
    kod: str
    nama: str
    keterangan: str | None = None


class ProfilResponse(BaseModel):
    id: int
    tapak_id: int
    kod: str
    nama: str
    keterangan: str | None
    aktif: bool

    class Config:
        from_attributes = True