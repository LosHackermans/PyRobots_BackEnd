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


# test upload robot
def test_create_robot():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "exist", "avatar": "", "script": "acd" , "fileName": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': "Robot created"}
    with db_session:
         delete (u for u in User if u.email == "famaf01@gmail.com")
         delete(r for r in Robot if r.name == "exist")

def test_create_robot_with_avatar():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "example_with_avatar",
              "avatar": "avatarpng", "script": "acd", "fileName": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': "Robot created"}
    with db_session:
        delete(r for r in Robot if r.name == "example_with_avatar")
        delete (u for u in User if u.email == "famaf01@gmail.com")


def test_invalid_token():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded2},
        json={"name": "example2", "avatar": "", "script": "acd", "fileName": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}


def test_create_bot_same_name():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)
        Robot(name="exist", script="abc", user=User.get(email = "famaf01@gmail.com"))
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "exist", "avatar": "", "script": "acd", "fileName": "acd"}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "robot with this name already exists"}
    with db_session:
        delete(r for r in Robot if r.name == "exist")
        delete (u for u in User if u.email == "famaf01@gmail.com")

def test_invalid_header():
    response = client.post(
        "/upload_robot",
        headers={"authorization": encoded},
        json={"name": "example2", "avatar": "", "script": "acd", "fileName": "acd"}
        )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}
