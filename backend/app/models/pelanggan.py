from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Pelanggan(Base):
    __tablename__ = "pelanggan"

    id = Column(Integer, primary_key=True)

    kod = Column(
        String(50),
        unique=True,
        nullable=False
    )
    nama = Column(
        String(255),
        nullable=False
    )
    keterangan = Column(Text)
    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())

    organisasi = relationship("Organisasi", back_populates="pelanggan")
