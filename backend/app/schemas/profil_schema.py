from pydantic import BaseModel


class ProfilCreate(BaseModel):
    tapak_id: int
    nama: str
    keterangan: str | None = None

    execution_type: str = "IMMEDIATE"
    cron_expression: str | None = None
    is_scheduled: bool = False
    report_template: str | None = "DEFAULT"
    report_format: str | None = "EXCEL"

class ProfilResponse(BaseModel):
    id: int
    tapak_id: int
    kod: str
    nama: str
    keterangan: str | None
    aktif: bool

    execution_type: str
    cron_expression: str | None
    is_scheduled: bool
    execution_status: str | None = None
    report_template: str | None = "DEFAULT"
    report_format: str | None = "EXCEL"

    tugasan_count: int = 0

    class Config:
        from_attributes = True