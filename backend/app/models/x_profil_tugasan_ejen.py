from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    TIMESTAMP,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.session import Base


class XProfilTugasanEjen(Base):
    __tablename__ = "x_profil_tugasan_ejen"

    id = Column(
        BigInteger,
        primary_key=True
    )

    profil_tugasan_id = Column(
        BigInteger,
        ForeignKey(
            "x_profil_tugasan.id",
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

    task_assignment = relationship(
        "XProfilTugasan",
        back_populates="agent_tasks"
    )

    agent = relationship(
        "Ejen",
        back_populates="task_assignments"
    )

    __table_args__ = (
        UniqueConstraint(
            "profil_tugasan_id",
            "ejen_id",
            name="uq_task_agent"
        ),
    )
