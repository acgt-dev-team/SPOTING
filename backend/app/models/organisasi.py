from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Organisasi(Base):
    __tablename__ = "organisasi"

    id = Column(Integer, primary_key=True)

    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"))

    kod = Column(String(50))
    nama = Column(String(255))
    keterangan = Column(Text)
    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())

    pelanggan = relationship("Pelanggan", back_populates="organisasi")
    sub_organisasi = relationship("SubOrganisasi", back_populates="organisasi")