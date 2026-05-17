from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import INET, JSON

class Ejen(SQLModel, table=True):
    id: int = Field(primary_key=True)
    ip_address: str = Field(sa_column=Column(INET, unique=True))
    tugasan_id: int = Field(foreign_key='tugasan.id')
    hasil_imbasan: list[dict] | None = Field(sa_column=Column(JSON, default=None))