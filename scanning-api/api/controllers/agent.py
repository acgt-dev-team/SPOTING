from fastapi import APIRouter, Request, HTTPException
from sqlmodel import select
from db.model.tugasan import Tugasan
from db.model.hasil_imbasan import HasilImbasan
from db.model.ejen import Ejen, EjenInit, EjenInitBody, EjenHasil, EjenHasilResponse
from db.model.profil_tugasan import ProfilTugasan, ProfilTugasanEjenResponse
from db.config import SessionDep
import os

router = APIRouter(prefix='/ejen')
platform_url = os.getenv('PLATFORM_URL')

@router.post(
    path='/init',
    tags=['Ejen'],
    response_model=EjenInit,
    summary='Ejen register'
)
async def agent_init(body: EjenInitBody, session: SessionDep):
    host_ip = body.host_ip
    tapak_id = body.tapak_id

    # Register agent in DB
    ejen = Ejen(
        ip_address=host_ip,
        tapak_id=tapak_id
    )
    session.add(ejen)
    session.commit()

    return {
        'platform_url': platform_url
    }

# @router.get(
#     path='/penjadualan',
#     tags=['Ejen'],
#     response_model=ProfilTugasanEjenResponse,
#     summary='Ejen check samada ada scheduled job'
# )
# async def agent_penjadualan(host_ip: str, session: SessionDep):
#     # Looking for x_profil
#     ejen = session.exec(select(Ejen).where(Ejen.ip_address == host_ip)).one()

#     profil_tugasan = session.exec(select(ProfilTugasan).where(
#         ProfilTugasan.tugasan_id == ejen.tugasan_id,
#         ProfilTugasan.jadualkan_pada != None
#     )).first()

#     return profil_tugasan

@router.post('/hasil', tags=['Ejen'], response_model=EjenHasilResponse)
async def hasil_imbasan(body: EjenHasil, session: SessionDep):
    hasil_imbasan = body.hasil_imbasan
    host_ip = body.host_ip

    try:
        stmt = select(Ejen).where(Ejen.ip_address == host_ip)
        ejen = session.exec(stmt).one()

        hasil = HasilImbasan(
            profil_tugasan_id=1,
            ejen_id=ejen.id,
            hasil=hasil_imbasan
        )
        session.add(hasil)
        session.commit()

        return {
            'status': 200,
            'message': 'Succeed'
        }
    except Exception:
        raise HTTPException(status_code=400, detail={ 'message': 'Failed'})
