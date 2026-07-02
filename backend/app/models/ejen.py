from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Ejen(Base):
    __tablename__ = "ejen"

    id = Column(BigInteger, primary_key=True, index=True)

    ip_address = Column(INET, unique=True, nullable=False)

    tapak_id = Column(
        BigInteger,
        ForeignKey("tapak.id"),
        nullable=False
    )

    tugasan_id = Column(
        BigInteger,
        ForeignKey("tugasan.id"),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    # Relationships
    tapak = relationship("Tapak")

    tugasan = relationship("Tugasan")

    hasil_imbasan = relationship(
        "HasilImbasan",
        back_populates="ejen",
        cascade="all, delete"
    )