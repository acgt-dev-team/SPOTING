from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.x_profil_tugasan import x_profil_tugasan

class Profil(Base):
    __tablename__ = "profil"

    id = Column(Integer, primary_key=True, index=True)
    tapak_id = Column(Integer, ForeignKey("tapak.id", ondelete="CASCADE"), nullable=False)

    kod = Column(String(50), unique=True, nullable=False)
    nama = Column(String(255), nullable=False)
    deskripsi = Column(Text)

    aktif = Column(Boolean, default=True)

    cipta_pada = Column(TIMESTAMP, server_default=func.now())
    kemaskini_pada = Column(TIMESTAMP, server_default=func.now())

    tapak = relationship("Tapak", back_populates="profil")

    profil_tugasan = relationship(
    "XProfilTugasan",
    back_populates="profil",
    cascade="all, delete"
)