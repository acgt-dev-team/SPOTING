from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    TIMESTAMP
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class XProfilEjen(Base):
    __tablename__ = "x_profil_ejen"

    id = Column(
        BigInteger,
        primary_key=True
    )

    profil_id = Column(
        BigInteger,
        ForeignKey(
            "profil.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    ejen_id = Column(
        BigInteger,
        ForeignKey(
            "ejen.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        server_default="Pending"
    )

    started_at = Column(
        TIMESTAMP,
        nullable=True
    )

    completed_at = Column(
        TIMESTAMP,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    profile = relationship(
        "Profil",
        back_populates="profile_agents"
    )

    agent = relationship(
        "Ejen",
        back_populates="profile_assignments"
    )
