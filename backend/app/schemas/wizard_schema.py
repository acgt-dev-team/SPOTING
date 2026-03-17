from pydantic import BaseModel, IPvAnyAddress
from typing import Optional


class WizardSetup(BaseModel):

    # hierarchy
    pelanggan: str
    organisasi: str
    sub_organisasi: str
    tapak: str
    profil: str

    # optional scheduling
    cronjob: Optional[str] = None

    # task
    task_name: str
    task_type: Optional[str] = None

    protocol: str

    ip_start: IPvAnyAddress
    ip_end: IPvAnyAddress
