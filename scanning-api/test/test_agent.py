from fastapi.testclient import TestClient
from db.config import get_session
from unittest.mock import MagicMock
from api.main import app
import os

client = TestClient(app)

platform_url = os.getenv('PLATFORM_URL')

def test_init():
    fake_session = MagicMock()

    app.dependency_overrides[get_session] = lambda: fake_session

    try:
        response = client.post(
            url='/ejen/init',
            json={ 'host_ip': f'127.0.0.1', 'tapak_id': 1 }
        )

        assert response.status_code == 200
        assert response.json() == { 'platform_url': platform_url}

        fake_session.add.assert_called_once()
        fake_session.commit.assert_called_once()
    finally:
        app.dependency_overrides.clear()

def test_hasil_imbasan():
    fake_session = MagicMock()
    fake_ejen_result = MagicMock()
    fake_tugasan_result = MagicMock()
    fake_profil_tugasan_result = MagicMock()

    fake_ejen_result.ip_address = '127.0.0.1'
    fake_tugasan_result.id = 1
    fake_profil_tugasan_result.id = 1

    fake_ejen = MagicMock()
    fake_tugasan = MagicMock()
    fake_profil_tugasan = MagicMock()

    fake_ejen.one.return_value = fake_ejen_result
    fake_tugasan.one.return_value = fake_tugasan_result
    fake_profil_tugasan.all.return_value = [fake_profil_tugasan_result]

    fake_session.exec.side_effect = [
        fake_ejen,
        fake_tugasan,
        fake_profil_tugasan
    ]

    app.dependency_overrides[get_session] = lambda: fake_session

    fake_hasil = [
        { 'test': 'Hello world' }
    ]

    try:
        response = client.post(
            url='/ejen/hasil',
            json={ 'host_ip': '127.0.0.1', 'hasil_imbasan': fake_hasil }
        )

        assert response.status_code == 200
        assert response.json() == { 'status': 200, 'message': 'Succeed' }
        fake_session.add.assert_called_once()
        fake_session.commit.assert_called_once()
    finally:
        app.dependency_overrides.clear()