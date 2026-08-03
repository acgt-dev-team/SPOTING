from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Organisasi(Base):
    __tablename__ = "organisasi"

    id = Column(Integer, primary_key=True)

    pelanggan_id = Column(
        Integer,
        ForeignKey(
            "pelanggan.id",
            ondelete="CASCADE"
        ),
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
    aktif = Column(Boolean, default=True)
    pegawai_tadbir = Column(
        String(64)
    )
    jawatan = Column(
        String(64)
    )

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())

    pelanggan = relationship("Pelanggan", back_populates="organisasi")
    sub_organisasi = relationship(
    "SubOrganisasi",
    back_populates="organisasi",
    cascade="all, delete"  # ✅ THIS FIXES DELETE
)
