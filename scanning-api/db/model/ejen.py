from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import INET, JSON
from pydantic import BaseModel, Field as PyField

class EjenInit(BaseModel):
    platform_url: str = PyField(examples=['http://ec2-56-68-97-215.ap-southeast-5.compute.amazonaws.com/'])

class EjenInitBody(BaseModel):
    host_ip: str = PyField(examples=['127.0.0.1'])

class EjenHasil(BaseModel):
    host_ip: str = PyField(examples=['127.0.0.1'])
    hasil_imbasan: dict = PyField(examples=['JSON string'])

class EjenHasilResponse(BaseModel):
    status: int = PyField(examples=[200])
    message: str = PyField(examples=['Succeed'])

class Ejen(SQLModel, table=True):
    id: int = Field(primary_key=True)
    ip_address: str = Field(sa_column=Column(INET, unique=True))
    tugasan_id: int = Field(foreign_key='tugasan.id')
    hasil_imbasan: list[dict] | None = Field(sa_column=Column(JSON, default=None))