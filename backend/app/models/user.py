from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    username = Column(String(24), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    aktif = Column(Boolean, default=True)
    force_password_change = Column(Boolean, default=True)
    deleted_at = Column(DateTime, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    pelanggan_id = Column(
        Integer,
        ForeignKey("pelanggan.id"),
        nullable=True
    )
