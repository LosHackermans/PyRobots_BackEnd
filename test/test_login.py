from fastapi.testclient import TestClient
from app.main import *
import jwt

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
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "nuevofamaf"}
    )
    assert response.status_code == 200
    assert response.json() == {'token': encoded}

def test_incorrect_password():
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "asd"}
    )
    assert response.status_code == 200
    assert response.json() == {'error': ' incorrect Password'}

def test_user_not_exist():
    response = client.post(
        "/login",
        json ={"email": 'famaf@gmail.com', "password": "asd"}
        )
    assert response.status_code == 200
    assert response.json() == {'error': 'User not exist'}