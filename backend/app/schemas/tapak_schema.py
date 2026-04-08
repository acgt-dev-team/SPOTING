from pydantic import BaseModel


class TapakCreate(BaseModel):
    sub_organisasi_id: int
    kod: str
    nama: str
    keterangan: str | None = None


class TapakResponse(BaseModel):
    id: int
    sub_organisasi_id: int
    kod: str
    nama: str
    keterangan: str | None
    aktif: bool

    class Config:
        from_attributes = True