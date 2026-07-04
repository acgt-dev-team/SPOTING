from pydantic import BaseModel


class AgentTask(BaseModel):
    profil_tugasan_id: int

    profil_id: int
    profil_nama: str

    tugasan_id: int
    nama: str
    kod: str

    protocol: str | None = None
    ip_start: str | None = None
    ip_end: str | None = None


class AgentTaskList(BaseModel):
    tasks: list[AgentTask]