from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from backend.app.database.session import Base


class SubOrganisasi(Base):

    __tablename__ = "sub_organisasi"

    id = Column(Integer, primary_key=True, index=True)

    organisasi_id = Column(Integer, ForeignKey("organisasi.id"), nullable=False)

    kod = Column(String(50), unique=True, nullable=False)
    nama = Column(String(255), nullable=False)

    deskripsi = Column(Text)

    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())