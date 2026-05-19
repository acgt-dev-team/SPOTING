from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class HasilImbasan(SQLModel, table=True):
    __tablename__ = "hasil_imbasan"

    id: int | None = Field(default=None, primary_key=True)

    profil_tugasan_id: int = Field(
        foreign_key="x_profil_tugasan.id"
    )

    ejen_id: int = Field(
        foreign_key="ejen.id"
    )

    hasil: list[dict] = Field(
        sa_column=Column(JSON)
    )

    created_at: datetime | None = Field(default_factory=datetime.utcnow)