from fastapi.testclient import TestClient
from app.main import *
import jwt
from fastapi.encoders import jsonable_encoder


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


#test upload robot
def test_create_robot():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "exist", "avatar":"", "script": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail':"Robot created"}

def test_create_robot_with_avatar():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "example1", "avatar": "avatarpng", "script": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail':"Robot created"}

def test_invalid_token():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded2},
        json = {"name": "example2", "avatar":"", "script": "acd"}
    )
    assert response.status_code == 200    
    assert response.json() == {'error': 'Invalid X-Token header'}

def test_create_bot_same_name():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "exist", "avatar":"", "script": "acd"}
    )
    assert response.status_code == 400    
    assert response.json() == {'detail': "robot with this name already exists"}