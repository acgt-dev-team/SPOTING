from unittest.mock import MagicMock
from scheduler.schedule_work import run_schedule

def test_run_schedule_work(monkeypatch):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'message': 'Imbasan bermula'
    }

    def mock_post(*args, **kwargs):
        return mock_response
    
    monkeypatch.setattr('requests.post', mock_post)

    fake_item = MagicMock()
    fake_item.tugasan_id = 1
    fake_item.status_id = 2

    fake_ejen = MagicMock()
    fake_ejen.ip_address = 'http://127.0.0.1'

    session = MagicMock()
    session.exec().all.side_effect = [
        [fake_item],
        [fake_ejen]
    ]

    run_schedule(session)

    assert fake_item.status_id == 2
    session.add.assert_called_once_with(fake_item)
    session.commit.assert_called()