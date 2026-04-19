from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class Cbom(SQLModel, table=True):
    __tablename__ = 'cbom_records'

    id: int = Field(primary_key=True)
    tugasan_id: int
    cbom_data: dict = Field(sa_column=Column(JSON), default_factory=dict)