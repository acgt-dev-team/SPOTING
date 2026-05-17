from fastapi import APIRouter, Request, HTTPException
from sqlmodel import select
from db.model.tugasan import Tugasan
from db.model.ejen import Ejen
from db.model.profil_tugasan import ProfilTugasan
from db.config import SessionDep
import os

router = APIRouter(prefix='/ejen')
platform_url = os.getenv('PLATFORM_URL')

@router.get('/init', tags=['Ejen'])
async def agent_init(session: SessionDep, request: Request):
    body = await request.json()

    host_ip = body['host_ip']
    stmt = select(Tugasan).where(
        Tugasan.ip_start <= host_ip,
        Tugasan.ip_end >= host_ip
    )
    tugasan = session.exec(stmt).one()

    # Register agent in DB
    ejen = Ejen(
        ip_address=host_ip,
        tugasan_id=tugasan.id
    )
    session.add(ejen)
    session.commit()

    return platform_url

@router.get('/penjadualan', tags=['Ejen'])
async def agent_penjadualan(session: SessionDep, request: Request):
    # Looking for x_profil
    body = await request.json()
    host_ip = body['host_ip']

    ejen = session.exec(select(Ejen).where(Ejen.ip_address == host_ip)).one()

    profil_tugasan = session.exec(select(ProfilTugasan).where(
        ProfilTugasan.tugasan_id == ejen.tugasan_id,
        ProfilTugasan.jadualkan_pada != None
    )).first()

    return profil_tugasan

@router.put('/hasil', tags=['Ejen'])
async def hasil_imbasan(request: Request, session: SessionDep):
    body = await request.json()

    hasil_imbasan = body['hasil_imbasan']
    host_ip = body['host_ip']

    try:
        stmt = select(Ejen).where(Ejen.ip_address == host_ip)
        ejen = session.exec(stmt).one()
        ejen.hasil_imbasan = hasil_imbasan
        session.add(ejen)
        session.commit()

        return {
            'status': 200,
            'message': 'Succeed'
        }
    except Exception:
        raise HTTPException(status_code=400, detail={ 'message': 'Failed'})
