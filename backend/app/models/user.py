from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=True)