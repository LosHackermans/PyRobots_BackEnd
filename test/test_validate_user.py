from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)

def test_validate_user():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = False, verify_token = "ABCDFG1")
    response = client.post(
        "/validate_user",
        json ={"email": 'famaf01@gmail.com', "token": "ABCDFG1"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "valid token"}
    with db_session:
        delete (u for u in User if u.email == "famaf01@gmail.com")

def test_validate_user_not_existst():
    response = client.post(
        "/validate_user",
        json ={"email": 'famaf@gmail.com', "token": "ABCDFG1"}
    )
    assert response.status_code == 200
    assert response.json() == {"error": "user not exists"}

def test_not_validate_user():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = False, verify_token = "ABCDFG1")
    response = client.post(
        "/validate_user",
        json ={"email": 'famaf01@gmail.com', "token": "21234"}
    )
    assert response.status_code == 200
    assert response.json() == {"error": "incorrect token"}
    with db_session:
        delete (u for u in User if u.email == "famaf01@gmail.com")
