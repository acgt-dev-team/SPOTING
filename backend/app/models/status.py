from sqlalchemy import Column, Integer, String
from app.database.session import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    kod_status = Column(String(50), unique=True, nullable=False)