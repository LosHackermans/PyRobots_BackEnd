from fastapi.testclient import TestClient
from app.main import *
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


# test create user
def test_create_user():
    response = client.post(
        '/create_user',
        json = {
                "username": "Juan8",
                "email": "pyrobotsok@gmail.com",
                "password": "password",
                "avatar": "asdasd"
                #"passwordRepeated": "password"
            })
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
    with db_session:
        delete(u for u in User if u.username == "Juan8")

def test_repeated_username():
    with db_session:
        User(
            username="testUser",
            email="testUser@gmail.com",
            password="testUser",
            is_validated=False
        )
    response = client.post(
        '/create_user',
        json = {
                "username": "testUser",
                "email": "testUsername@gmail.com",
                "password": "password",
                "avatar": "",
                "passwordRepeated": "password"
            })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User with this username already exists"}
    with db_session:
        delete(u for u in User if u.username == "testUser")


def test_repeated_email():
    with db_session:
        User(
            username="testEmail",
            email="testEmail@gmail.com",
            password="password",
            is_validated=False
        )
    response = client.post(
        '/create_user',
        json = {
                "username": "testEmail_2",
                "email": "testEmail@gmail.com",
                "password": "password",
                "avatar": "",
                "passwordRepeated": "password"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this email already exists"}
    with db_session:
        delete(u for u in User if u.username == "testEmail")


def test_bad_password():
    response = client.post(
        '/create_user',
        json = {
                "username": "testPassword",
                "email": "testPassword@gmail.com",
                "password": "pass",
                "avatar": "",
                "passwordRepeated": "pass"
            })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The password must have a minimum of 8 characters"}


""""
def test_bad_repeated_password():
    response = client.post(
        '/create_user',
        json = {
                "username": "testPassword2",
                "email": "testPassword2@gmail.com",
                "password": "password",
                "passwordRepeated": "password2"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords do not match"} 
"""
