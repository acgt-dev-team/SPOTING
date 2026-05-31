from sqlmodel import Session, select
from db.config import engine
from db.model.profil_tugasan import ProfilTugasan
from db.model.ejen import Ejen
from datetime import datetime
import requests
import os

agent_url = os.getenv('AGENT_URL')

with Session(engine) as session:
    now = datetime.now()
    stmt = select(ProfilTugasan).where(
        ProfilTugasan.status_id == 2,
        ProfilTugasan.jadualkan_pada <= now
    )
    list_tugasan = session.exec(stmt).all()

    for item in list_tugasan:

        ejen_list = session.exec(select(Ejen).where(Ejen.tugasan_id == item.tugasan_id)).all()

        for ejen in ejen_list:
            url = f'{ejen.ip_address}/imbas'

            try:
                body = {
                    'type': 'fast'
                }
                response = requests.post(url, json=body)
                res_data = response.json()

                if res_data['message'] == 'Imbasan bermula':
                    item.status_id = 2
                    session.add(item)
                    session.commit()

            except Exception as e:
                print('error =', e)