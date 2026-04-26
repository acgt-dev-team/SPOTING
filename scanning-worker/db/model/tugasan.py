from sqlmodel import SQLModel, Field

class Tugasan(SQLModel, table=True):
    __tablename__ = 'tugasan'

    id: int = Field(primary_key=True)
    ip_start: str
    ip_end: str