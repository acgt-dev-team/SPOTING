from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class HasilImbasan(Base):
    __tablename__ = "hasil_imbasan"

    id = Column(BigInteger, primary_key=True, index=True)

    profil_tugasan_id = Column(
        BigInteger,
        ForeignKey("x_profil_tugasan.id", ondelete="CASCADE"),
        nullable=False
    )

    ejen_id = Column(
        BigInteger,
        ForeignKey("ejen.id", ondelete="CASCADE"),
        nullable=False
    )

    hasil = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    # Relationships
    ejen = relationship(
        "Ejen",
        back_populates="hasil_imbasan"
    )

    profil_tugasan = relationship(
        "XProfilTugasan"
    )