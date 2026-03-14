from pydantic import BaseModel


class WizardSetup(BaseModel):

    pelanggan: str
    organisasi: str
    sub_organisasi: str
    tapak: str

    profil: str
    cronjob: str | None = None

    task_name: str
    task_type: str | None = None
    protocol: str
    ip_start: str
    ip_end: str