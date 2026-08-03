from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class SubOrganisasi(Base):
    __tablename__ = "sub_organisasi"

    id = Column(Integer, primary_key=True)

    organisasi_id = Column(
        Integer,
        ForeignKey("organisasi.id", ondelete="CASCADE"),
        nullable=False
    )
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
    pegawai_tadbir = Column(String(64))
    jawatan = Column(String(64))
    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())

    organisasi = relationship(
        "Organisasi",
        back_populates="sub_organisasi"
    )

    tapak = relationship(
        "Tapak",
        back_populates="sub_organisasi",
        cascade="all, delete"  # optional but good
    )
