from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Tugasan(Base):
    __tablename__ = "tugasan"

    id = Column(Integer, primary_key=True, index=True)

    nama = Column(String(255))

    kod = Column(String(50))  # ✅ ADD THIS

    protocol = Column(String(10))  # ✅ ADD THIS
    ip_start = Column(String(45))  # ✅ ADD THIS
    ip_end = Column(String(45))    # ✅ ADD THIS

    keterangan = Column(Text)

    aktif = Column(Boolean, default=True)

    jenis_id = Column(Integer, ForeignKey("jenis_tugasan.id"))  # ✅ ADD THIS

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())

    profil_tugasan = relationship(
        "XProfilTugasan",
        back_populates="tugasan",
        cascade="all, delete"
    )