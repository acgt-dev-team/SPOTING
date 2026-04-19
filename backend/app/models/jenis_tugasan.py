from sqlalchemy import Column, Integer, String
from app.database.session import Base

class JenisTugasan(Base):
    __tablename__ = "jenis_tugasan"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(255))