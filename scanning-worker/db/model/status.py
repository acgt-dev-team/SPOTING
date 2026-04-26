from sqlmodel import SQLModel, Field

class Status(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kod_status: str