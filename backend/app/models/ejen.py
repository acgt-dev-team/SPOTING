from sqlalchemy import (
    Column,
    BigInteger,
    TIMESTAMP,
    ForeignKey,
    String
)
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Ejen(Base):
    __tablename__ = "ejen"

    id = Column(BigInteger, primary_key=True)

    ip_address = Column(INET, unique=True, nullable=False)

    tapak_id = Column(
        BigInteger,
        ForeignKey("tapak.id"),
        nullable=False
    )
    
    machine_id = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False
    )

    hostname = Column(
        String(255),
        nullable=False
    )

    profile_id = Column(
        BigInteger,
        ForeignKey("profil.id"),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        server_default="Running"
    )

    last_seen = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    # Relationships
    tapak = relationship("Tapak")
    profile = relationship(
        "Profil",
        back_populates="agents"
    )


    hasil_imbasan = relationship(
        "HasilImbasan",
        back_populates="ejen",
        cascade="all, delete"
    )
    
    
    profile_assignments = relationship(
        "XProfilEjen",
        back_populates="agent",
        cascade="all, delete-orphan"
    )
    
    task_assignments = relationship(
        "XProfilTugasanEjen",
        back_populates="agent",
        cascade="all, delete-orphan"
    )
