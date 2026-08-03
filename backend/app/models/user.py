from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database.session import Base
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nama = Column(
        String,
        nullable=True
    )
    username = Column(
        String(50),
        unique=True,
        nullable=False
    )
    password = Column(
        String(255),
        nullable=False
    )
    role = Column(
        String(20),
        nullable=False,
        default="user"
    )
    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
    aktif = Column(Boolean, default=True)
    force_password_change = Column(Boolean, default=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    pelanggan_id = Column(
        Integer,
        ForeignKey("pelanggan.id"),
        nullable=True
    )
