from .main import *
from fastapi.testclient import TestClient
import jwt


client = TestClient(app)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
dummy_user = {
    "email": "famaf01@gmail.com",
    "password": "nuevofamaf"
}

encoded_jwt = jwt.encode(dummy_user, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")

encoded_jwt2 = jwt.encode(dummy_user2, SECRET_KEY, algorithm=ALGORITHM)
encoded2 = encoded_jwt2.decode("utf-8")


#test upload robot
def test_read_main():
    response = client.post(
        "/upload_robot",
        headers={"Authotization": "Bearer " + encoded},
        json = {"name": "example", "script": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail':"Robot created"}

def test_bad_create_item():
    response = client.post(
        "/upload_robot",
        headers={"Authotization": "Bearer " + encoded2},
        json = {"name": "example", "script": "acd"}
    )
    assert response.status_code == 200    
    assert response.json() == {'error': 'Invalid X-Token header'}

data = jsonable_encoder(dummy_user)
encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")

#test login
def test_read_main2():
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "nuevofamaf"}
    )
    assert response.status_code == 200
    assert response.json() == {'token': encoded}

def test_bad_read_main2():
    response = client.post(
        "/login",
        json ={"email": 'famaf01@gmail.com', "password": "asd"}
    )
    assert response.status_code == 200
    assert response.json() == {'error': ' incorrect Password'}
