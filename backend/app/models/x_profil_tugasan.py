from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.session import Base
from sqlalchemy import UniqueConstraint

class XProfilTugasan(Base):
    __tablename__ = "x_profil_tugasan"

    # actual DB primary key
    id = Column(Integer, primary_key=True)

    profil_id = Column(
        Integer,
        ForeignKey("profil.id", ondelete="CASCADE"),
        nullable=False
    )

    tugasan_id = Column(
        Integer,
        ForeignKey("tugasan.id", ondelete="CASCADE"),
        nullable=False
    )

    status_id = Column(
        Integer,
        ForeignKey("status.id")
    )

    jadualkan_pada = Column(TIMESTAMP, nullable=True)
    selesai_pada = Column(TIMESTAMP, nullable=True)

    profil = relationship(
        "Profil",
        back_populates="profil_tugasan"
    )

    tugasan = relationship(
        "Tugasan",
        back_populates="profil_tugasan"
    )
    profil_tugasan = relationship(
        "XProfilTugasan",
        back_populates="hasil_imbasan"
    )
    hasil_imbasan = relationship(
        "HasilImbasan",
        back_populates="profil_tugasan",
        cascade="all, delete"
    )
    status = relationship(
        "Status",
        back_populates="profil_tugasan"
    )
    
    __table_args__ = (
        UniqueConstraint(
            "profil_id",
            "tugasan_id",
            name="unique_profil_tugasan"
        ),
    )
