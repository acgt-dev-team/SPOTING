from fastapi import FastAPI, Depends
from fastapi.requests import Request
from sqlmodel import Session, select
from db.config import get_session
from typing import Annotated
from db.model.profil_tugasan import ProfilTugasan
from db.model.tugasan import Tugasan
from .publish_queue import queue_tugasan
import requests
import subprocess
from datetime import datetime
import os

app = FastAPI()
agent_url = os.getenv('AGENT_URL')

@app.get('/test')
def testing():
    return { 'message': 'API successfully instantiate' }

@app.post('/imbasan', tags=['Tugasan'])
async def imbasan(request: Request, session: Annotated[Session, Depends(get_session)]):
    body = await request.json()
    profil_tugasan_id = body['profil_tugasan_id']
    penjadualan = body.get('penjadualan')

    profil_tugasan = session.get(ProfilTugasan, profil_tugasan_id)
    stmt = select(Tugasan).where(Tugasan.id == profil_tugasan.tugasan_id)
    tugasan = session.exec(stmt).one()

    # Execute now, instantly
    if not penjadualan:
        agent_data = {
            'profil_tugasan_id': profil_tugasan_id,
            'ip': [tugasan.ip_start, tugasan.ip_end]
        }

        # Call agent to start scanning
        try:
            response = requests.post(f'{agent_url}/mula-imbasan', json=agent_data)
            res_data = response.json()
            if res_data['message'] == 'Imbasan bermula':
                profil_tugasan.status = 2
                session.add(profil_tugasan)
                session.commit()

            data = {
                'mesej': 'berjaya',
            }

            return data
        except Exception as e:
            print('error =', e)


# @app.post('/schedule-job', tags=['Tugasan'])
# async def schedule_job(request: Request):
#     body = await request.json()
#     tugasan_id = body['tugasan_id']
#     schedule = body['jadualkan_pada']

#     dt = datetime.strptime(schedule, '%Y-%m-%d %H:%M:%S')
#     day = dt.day
#     month = dt.month
#     hour = dt.hour
#     minute = dt.minute

#     cron = f'{minute} {hour} {day} {month} *'

#     new_job = f'{cron} curl http://localhost:8010/agct-agent/{tugasan_id}'

#     # Get existing cronjob
#     existing = subprocess.run(['crontab', '-l'], capture_output=True, text=True)

#     cron_content = existing.stdout if existing.returncode == 0 else ''

#     # Add new job
#     cron_content += '\n' + new_job + '\n'

#     # Write back
#     subprocess.run(['crontab', '-'], input=cron_content, text=True)

#     data = {
#         'tugasan_id': tugasan_id,
#         'status': -1
#     }
#     return data