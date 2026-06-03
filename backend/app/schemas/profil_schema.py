from pydantic import BaseModel
from datetime import datetime


class ProfilCreate(BaseModel):
    tapak_id: int
    nama: str
    keterangan: str | None = None

    execution_type: str = "IMMEDIATE"
    scheduled_at: datetime | None = None   # ✅ FIXED
    is_scheduled: bool = False

    cron_enabled: bool = False
    frequency: str | None = None
    cron_expression: str | None = None

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
    scheduled_at: datetime | None = None   # ✅ FIXED
    is_scheduled: bool
    execution_status: str | None = None

    cron_enabled: bool = False
    frequency: str | None = None
    cron_expression: str | None = None

    report_template: str | None = "DEFAULT"
    report_format: str | None = "EXCEL"

    tugasan_count: int = 0

    class Config:
        from_attributes = True