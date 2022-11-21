from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
dummy_user = {
    "email": "famaf01@gmail.com",
    "password": "nuevofamaf"
}
dummy_user2 = {
    "email": "famaf02@gmail.com",
    "password": "nuevofamaf"
}
encoded_jwt = jwt.encode(dummy_user, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")

encoded_jwt2 = jwt.encode(dummy_user2, SECRET_KEY, algorithm=ALGORITHM)
encoded2 = encoded_jwt2.decode("utf-8")



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