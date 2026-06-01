from db.config import engine
from sqlmodel import select
from sqlmodel import Session
from db.model.profil_tugasan import ProfilTugasan
from db.model.ejen import Ejen
from db.model.tugasan import Tugasan
import ipaddress
from datetime import datetime

def run_check(session):
    stmt = select(ProfilTugasan).where(ProfilTugasan.status_id == 1)
    profil_tugasan_list = session.exec(stmt).all()

    for item in profil_tugasan_list:
        stmt_tugasan = select(Tugasan).where(Tugasan.id == item.tugasan_id)
        tugasan = session.exec(stmt_tugasan).one()

        total_ip = ( int(ipaddress(tugasan.ip_start)) - int(ipaddress(tugasan.ip_end)) ) + 1

        stmt = select(Ejen).where(Ejen.tugasan_id == item.tugasan_id)
        ejen = session.exec(stmt).all()

        if len(ejen) >= total_ip:
            item.selesai_pada = datetime.now()
            session.add(item)
            session.commit()

if __name__ == '__main__':
    with Session(engine) as session:
        run_check(session)