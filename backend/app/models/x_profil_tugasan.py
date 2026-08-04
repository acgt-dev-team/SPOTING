from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base


class XProfilTugasan(Base):
    __tablename__ = "x_profil_tugasan"

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

    jadualkan_pada = Column(TIMESTAMP)
    selesai_pada = Column(TIMESTAMP)

    profil = relationship(
        "Profil",
        back_populates="profil_tugasan"
    )

    tugasan = relationship(
        "Tugasan",
        back_populates="profil_tugasan"
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
