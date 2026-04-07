from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base

class XProfilTugasan(Base):
    __tablename__ = "x_profil_tugasan"

    profil_id = Column(Integer, ForeignKey("profil.id", ondelete="CASCADE"), primary_key=True)
    tugasan_id = Column(Integer, ForeignKey("tugasan.id", ondelete="CASCADE"), primary_key=True)

    status = Column(Integer, default=-1)  # -1, 0, 1
    jadualkan_pada = Column(TIMESTAMP, nullable=True)
    selesai_pada = Column(TIMESTAMP, nullable=True)

    # relationships
    profil = relationship("Profil", back_populates="profil_tugasan")
    tugasan = relationship("Tugasan", back_populates="profil_tugasan")