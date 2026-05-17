from fastapi import APIRouter, Request
from db.config import SessionDep
from sqlmodel import select
from db.model.profil_tugasan import ProfilTugasan
from db.model.ejen import Ejen
import requests
import os

agent_url = os.getenv('AGENT_URL')
router = APIRouter(prefix='/pengguna')

@router.post('/imbas', tags=['Pengguna'])
async def imbasan(request: Request, session: SessionDep):
    body = await request.json()
    profil_tugasan_id = body['profil_tugasan_id']

    profil_tugasan = session.get(ProfilTugasan, profil_tugasan_id)

    query = select(Ejen).where(Ejen.tugasan_id == profil_tugasan.tugasan_id)
    ejen = session.exec(query).all()

    for e in ejen:
        # Execute scan
        ip_address = e.ip_address
        url = f'{ip_address}/imbas'
        try:
            response = requests.get(url)
            res_data = response.json()

            if res_data['message'] == 'Imbasan bermula':
                profil_tugasan.status_id = 2
                session.add(profil_tugasan)
                session.commit()

            data = {
                'mesej': 'berjaya',
            }

            return data
        except Exception as e:
            print('error =', e)
