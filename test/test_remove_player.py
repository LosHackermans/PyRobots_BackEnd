from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)


def test_invalid_header():
    response = client.post(
        "/abandon/{match_id}",
        headers={"authorization": encoded},
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}
