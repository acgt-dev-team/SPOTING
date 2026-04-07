from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.x_profil_tugasan import x_profil_tugasan

class Tugasan(Base):
    __tablename__ = "tugasan"

    id = Column(Integer, primary_key=True, index=True)

    nama = Column(String(255))
    jenis = Column(String(100))
    protocol = Column(String(10))

    ip_start = Column(String(45))
    ip_end = Column(String(45))

    cipta_pada = Column(TIMESTAMP, server_default=func.now())

    profil = relationship(
        "Profil",
        secondary=x_profil_tugasan,
        back_populates="tugasan"
    )