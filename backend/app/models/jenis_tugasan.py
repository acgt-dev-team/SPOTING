from sqlalchemy import Column, Integer, String
from app.database.session import Base
from sqlalchemy.orm import relationship

class JenisTugasan(Base):
    __tablename__ = "jenis_tugasan"

    id = Column(Integer, primary_key=True)
    nama = Column(
        String(100),
        nullable=False
    )
    
    tugasan = relationship(
        "Tugasan",
        back_populates="jenis_tugasan"
    )
