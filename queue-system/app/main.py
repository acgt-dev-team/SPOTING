from fastapi import FastAPI
from fastapi.requests import Request
from .model.cbom_model import ScanCbom
from .publish_queue import queue_tugasan
import requests
import subprocess
from datetime import datetime

app = FastAPI()

@app.get('/test')
def testing():
    return { 'message': 'API successfully instantiate' }

@app.post('/imbasan', tags=['Tugasan'])
async def imbasan(request: Request):
    body = await request.json()
    tugasan_id = body['tugasan_id']
    penjadualan = body['penjadualan']

    # Execute now, instantly
    if not penjadualan:
        agent_data = {
            'tugasan_id': tugasan_id,
            'ip': ['127.0.0.125', '127.0.0.230']
        }

        # Call agent to start scanning
        print('Make request to agent to scan')
        response = requests.post(f'http://localhost:8010/agct-agent', agent_data)
        res_data = response.json()
        if res_data['message'] == 'Imbasan bermula':
            print('Scaning has started')

        data = {
            'tugasan_id': tugasan_id,
            'status': 1
        }

        return data

@app.post('/schedule-job', tags=['Tugasan'])
async def schedule_job(request: Request):
    body = await request.json()
    tugasan_id = body['tugasan_id']
    schedule = body['jadualkan_pada']

    dt = datetime.strptime(schedule, '%Y-%m-%d %H:%M:%S')
    day = dt.day
    month = dt.month
    hour = dt.hour
    minute = dt.minute

    cron = f'{minute} {hour} {day} {month} *'

    new_job = f'{cron} curl http://localhost:8010/agct-agent/{tugasan_id}'

    # Get existing cronjob
    existing = subprocess.run(['crontab', '-l'], capture_output=True, text=True)

    cron_content = existing.stdout if existing.returncode == 0 else ''

    # Add new job
    cron_content += '\n' + new_job + '\n'

    # Write back
    subprocess.run(['crontab', '-'], input=cron_content, text=True)

    data = {
        'tugasan_id': tugasan_id,
        'status': -1
    }
    return data

@app.post('/receive-cbom', tags=['Tugasan'])
def receive_cbom_data(data: ScanCbom):
    queue_tugasan(data.model_dump())
    return True