from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Tugasan(Base):
    __tablename__ = "tugasan"

    id = Column(Integer, primary_key=True, index=True)

    nama = Column(String(255))
    jenis_id = Column(Integer, ForeignKey("jenis_tugasan.id"))
    protocol = Column(String(10))

    ip_start = Column(String(45))
    ip_end = Column(String(45))

    cipta_pada = Column(TIMESTAMP, server_default=func.now())

    profil_tugasan = relationship(
    "XProfilTugasan",
    back_populates="tugasan",
    cascade="all, delete"
)