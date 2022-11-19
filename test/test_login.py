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

#test login
def test_login():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "nuevofamaf"}
    )
    assert response.status_code == 200
    assert response.json() == {'token': encoded}
    with db_session:
        delete (u for u in User if u.email == "famaf01@gmail.com")

def test_incorrect_password():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "asd"}
    )
    assert response.status_code == 200
    assert response.json() == {'error': ' incorrect Password'}
    with db_session:
        delete (u for u in User if u.email == "famaf01@gmail.com")

def test_login_not_verify():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = False)
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "nuevofamaf"}
    )
    assert response.status_code == 200
    assert response.json() == {'error': ' not verify'}
    with db_session:
        delete (u for u in User if u.email == "famaf01@gmail.com")


def test_user_not_exist():
    response = client.post(
        "/login",
        json ={"email": 'famaf@gmail.com', "password": "asd"}
        )
    assert response.status_code == 200
    assert response.json() == {'error': 'User not exist'}