from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from app.database.session import Base


class Tugasan(Base):

    __tablename__ = "tugasan"

    id = Column(Integer, primary_key=True, index=True)

    profil_id = Column(Integer, ForeignKey("profil.id"), nullable=False)

    nama = Column(String(255))
    jenis = Column(String(100))
    protocol = Column(String(10))

    ip_start = Column(String(45))
    ip_end = Column(String(45))

    cipta_pada = Column(TIMESTAMP, server_default=func.now())