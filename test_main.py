from .main import *
from fastapi.testclient import TestClient


client = TestClient(app)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
dummy_user = {
    "email": "famaf01@gmail.com",
    "password": "nuevofamaf"
}
data = jsonable_encoder(dummy_user)
encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")
#test
def test_read_main():
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "nuevofamaf"}
    )
    assert response.status_code == 200
    assert response.json() == {'token': encoded}

def test_bad_read_main():
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "asd"}
    )
    assert response.status_code == 200
    assert response.json() == {'error': ' incorrect Password'}
