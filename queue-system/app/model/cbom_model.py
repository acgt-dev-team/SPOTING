from sqlmodel import SQLModel, Field, Column
from pydantic import BaseModel
from sqlalchemy import JSON

class Cbom(SQLModel, table=True):
    __tablename__ = 'cbom_records'

    id: int = Field(primary_key=True)
    tugasan_id: int
    cbom_data: list[dict] = Field(sa_column=Column(JSON), default_factory=list)

class ScanCbom(BaseModel):
    tugasan_id: int
    cbom_data: dict
