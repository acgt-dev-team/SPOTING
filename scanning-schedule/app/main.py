from sqlmodel import Session, select
from db.config import engine
from db.model.profil_tugasan import ProfilTugasan
from db.model.tugasan import Tugasan
from datetime import datetime
import requests
import os

agent_url = os.getenv('AGENT_URL')

with Session(engine) as session:
    now = datetime.now()
    stmt = select(ProfilTugasan).where(
        ProfilTugasan.status == -1,
        ProfilTugasan.jadualkan_pada <= now
    )
    list_tugasan = session.exec(stmt).all()

    for item in list_tugasan:

        tugasan = session.get(Tugasan, item.tugasan_id)

        profil_tugasan_id = item.id
        agent_data = {
            'profil_tugasan_id': profil_tugasan_id,
            'ip': [tugasan.ip_start, tugasan.ip_end]
        }

        # Call agent to start scanning
        try:
            response = requests.post(f'{agent_url}/mula-imbasan', json=agent_data)
            res_data = response.json()
            if res_data['message'] == 'Imbasan bermula':
                item.status_id = 3
                session.add(item)
                session.commit()

        except Exception as e:
            print('error =', e)