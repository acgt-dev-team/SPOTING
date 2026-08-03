from sqlalchemy import Column, Integer, String
from app.database.session import Base
from sqlalchemy.orm import relationship

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    kod_status = Column(
        String(20),
        unique=True,
        nullable=False
    )
    profil_tugasan = relationship(
        "XProfilTugasan",
        back_populates="status"
    )
