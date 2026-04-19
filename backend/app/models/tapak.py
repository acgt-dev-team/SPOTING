from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Tapak(Base):
    __tablename__ = "tapak"

    id = Column(Integer, primary_key=True, index=True)

    sub_organisasi_id = Column(
        Integer,
        ForeignKey("sub_organisasi.id", ondelete="CASCADE"),
        nullable=False
    )

    kod = Column(String(50), unique=True, nullable=False)
    nama = Column(String(255), nullable=False)

    keterangan = Column(Text)

    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    alamat_baris_1 = Column(String(128))
    alamat_baris_2 = Column(String(128))
    bandar = Column(String(64))
    negeri = Column(String(64))
    negara = Column(String(64))
    pegawai_tadbir = Column(String(64))
    jawatan = Column(String(64))

    sub_organisasi = relationship("SubOrganisasi", back_populates="tapak")

    profil = relationship(
        "Profil",
        back_populates="tapak",
        cascade="all, delete-orphan"
    )