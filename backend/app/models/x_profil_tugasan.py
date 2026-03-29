from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.session import Base

x_profil_tugasan = Table(
    "x_profil_tugasan",
    Base.metadata,
    Column("profil_id", Integer, ForeignKey("profil.id", ondelete="CASCADE"), primary_key=True),
    Column("tugasan_id", Integer, ForeignKey("tugasan.id", ondelete="CASCADE"), primary_key=True),
)