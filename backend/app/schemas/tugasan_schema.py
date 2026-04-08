from pydantic import BaseModel


class TugasanCreate(BaseModel):
    nama: str
    kod: str
    keterangan: str | None = None
    jenis_id: int


class TugasanResponse(BaseModel):
    id: int
    nama: str
    kod: str
    keterangan: str | None
    jenis_id: int
    aktif: bool

    class Config:
        from_attributes = True