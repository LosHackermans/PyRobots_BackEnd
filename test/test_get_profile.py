from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)



def test_invalid_header():
    
    response = client.post(
        "/profile",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}


def test_get_profile_data():

    user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
    
    response = client.post(
        "/profile",
        headers={"authorization": "Bearer " + encoded}
    )

    assert response.status_code == 200
    assert response.json() == {
        "username": user_test.username,
        "email": user_test.email,
        "avatar": user_test.avatar #puede ser Vacio
    }