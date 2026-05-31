from fastapi import APIRouter, Request
from db.config import SessionDep
from sqlmodel import select
from db.model.profil_tugasan import ProfilTugasan
from db.model.ejen import Ejen
from db.model.hasil_imbasan import HasilImbasan

import requests
import os


router = APIRouter(prefix='/pengguna')


@router.post('/imbas', tags=['Pengguna'])
async def imbasan(request: Request, session: SessionDep):

    body = await request.json()

    profil_tugasan_id = body['profil_tugasan_id']

    profil_tugasan = session.get(
        ProfilTugasan,
        profil_tugasan_id
    )

    query = select(Ejen).where(
        Ejen.tugasan_id == profil_tugasan.tugasan_id
    )

    ejen = session.exec(query).all()

    for e in ejen:

        # ==========================================
        # EXECUTE SCAN
        # ==========================================

        ip_address = e.ip_address

        # IMPORTANT
        AGENT_PORT = os.getenv("AGENT_PORT", "9001")

        url = f'http://{ip_address}:{AGENT_PORT}/imbas'

        try:

            response = requests.get(url)

            response.raise_for_status()

            res_data = response.json()

            print('SCAN RESULT =', res_data)

            # ==========================================
            # SAVE RESULT INTO DATABASE
            # ==========================================

            scan_result = HasilImbasan(
                profil_tugasan_id=profil_tugasan_id,
                ejen_id=e.id,
                hasil=res_data.get('hasil_imbasan')
            )

            session.add(scan_result)
            session.commit()

            # ==========================================
            # UPDATE STATUS
            # ==========================================

            if res_data.get('message') == 'Imbasan berjaya':

                profil_tugasan.status_id = 3

            else:

                profil_tugasan.status_id = 2

            session.add(profil_tugasan)

            session.commit()

        except Exception as ex:

            print('error =', ex)

            profil_tugasan.status_id = 4

            session.add(profil_tugasan)

            session.commit()

    return {
    'mesej': 'berjaya',
    'hasil_imbasan': [
        {
            'ip_address': str(e.ip_address),
            'hasil': res_data.get('hasil_imbasan')
        }
        for e in ejen
    ]
}