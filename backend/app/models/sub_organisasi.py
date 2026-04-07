from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class SubOrganisasi(Base):  # ✅ CORRECT CLASS NAME
    __tablename__ = "sub_organisasi"

    id = Column(Integer, primary_key=True, index=True)

    organisasi_id = Column(
        Integer,
        ForeignKey("organisasi.id", ondelete="CASCADE"),
        nullable=False
    )

    kod = Column(String(50), unique=True, nullable=False)
    nama = Column(String(255), nullable=False)
    deskripsi = Column(Text)

    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    organisasi = relationship(
        "Organisasi",
        back_populates="sub_organisasi"
    )

    tapak = relationship(
        "Tapak",
        back_populates="sub_organisasi",
        cascade="all, delete-orphan"
    )