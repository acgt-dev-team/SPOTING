from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime 

class HasilImbasan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    profil_tugasan_id: int = Field(foreign_key='x_profil_tugasan.id')
    ejen_id: int = Field(foreign_key='ejen.id')
    created_at: datetime = Field(default=datetime.now())
    hasil: list[dict] = Field(sa_column=Column(JSON), default_factory=list)
