from sqlmodel import SQLModel, Field, Column
from pydantic import BaseModel
from sqlalchemy import JSON

class Imbasan(SQLModel, table=True):
    __tablename__ = 'hasil_imbasan'

    id: int = Field(primary_key=True)
    x_profil_tugasan_id: int = Field(foreign_key='x_profil_tugasan.id')
    data_imbasan: list[dict] = Field(sa_column=Column(JSON), default_factory=list)