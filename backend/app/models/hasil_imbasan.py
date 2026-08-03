from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    TIMESTAMP,
    Text
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.session import Base


class HasilImbasan(Base):
    __tablename__ = "hasil_imbasan"

    id = Column(BigInteger, primary_key=True)

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
    
    machine_id = Column(
        UUID(as_uuid=True),
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
    
    prev_hash = Column(
        Text,
        nullable=True
    )
    row_hash = Column(
        Text,
        nullable=True
    )

    # Relationships
    ejen = relationship(
        "Ejen",
        back_populates="hasil_imbasan"
    )

    profil_tugasan = relationship(
        "XProfilTugasan",
        back_populates="hasil_imbasan"
    )
