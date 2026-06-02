from sqlmodel import SQLModel, Field

class Tapak(SQLModel, table=True):
    id: int = Field(primary_key=True)