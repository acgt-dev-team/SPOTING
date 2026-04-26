from fastapi import FastAPI, Depends
from fastapi.requests import Request
from sqlmodel import Session, select
from db.config import get_session
from typing import Annotated
from db.model.profil_tugasan import ProfilTugasan
from db.model.tugasan import Tugasan
import requests
import os

app = FastAPI()
agent_url = os.getenv('AGENT_URL')

SessionDep = Annotated[Session, Depends(get_session)]

@app.get('/test')
def testing():
    return { 'message': 'API successfully instantiate' }

@app.post('/imbasan', tags=['Tugasan'])
async def imbasan(request: Request, session: SessionDep):
    body = await request.json()
    profil_tugasan_id = body['profil_tugasan_id']
    penjadualan = body.get('penjadualan')

    profil_tugasan = session.get(ProfilTugasan, profil_tugasan_id)
    stmt = select(Tugasan).where(Tugasan.id == profil_tugasan.tugasan_id)
    tugasan = session.exec(stmt).one()

    if not penjadualan:
        agent_data = {
            'profil_tugasan_id': profil_tugasan_id,
            'ip': [tugasan.ip_start, tugasan.ip_end]
        }

        try:
            response = requests.post(f'{agent_url}/mula-imbasan', json=agent_data)
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