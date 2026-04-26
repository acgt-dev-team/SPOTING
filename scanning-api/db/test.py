from .config import engine
from sqlmodel import Session, select
from .model.profil_tugasan import ProfilTugasan

with Session(engine) as session:
    stmt = select(ProfilTugasan)
    tugasan = session.exec(stmt).all()

    for item in tugasan:
        print(item.jadualkan_pada)