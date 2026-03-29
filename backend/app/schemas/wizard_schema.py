from pydantic import BaseModel, IPvAnyAddress
from typing import Optional

class WizardSetup(BaseModel):
    pelanggan: str
    organisasi: str
    sub_organisasi: str
    tapak: str
    profil: str

    cronjob: Optional[str] = None

    task_name: str
    jenis: Optional[str] = None
    protocol: str

    ip_start: IPvAnyAddress
    ip_end: IPvAnyAddress