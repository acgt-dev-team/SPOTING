from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import INET

class Tugasan(SQLModel, table=True):
    __tablename__ = 'tugasan'

    id: int = Field(primary_key=True)
    ip_start: str = Field(sa_column=Column(INET))
    ip_end: str = Field(sa_column=Column(INET))