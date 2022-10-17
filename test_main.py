
from fastapi.testclient import TestClient
from .main import *



client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_user():
    response = client.post(
        '/signup',
        json = {
                "username": "Juan2",
                "email": "juanpereez@gmail.com",
                "password": "password"
            })
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_repeated_username():
    with db_session:
        User(
            username = "testUser",
            email = "testUser@gmail.com",
            password = "testUser",
            is_validated = False
            )
    response = client.post(
        '/signup',
        json = {
                "username": "testUser",
                "email": "testUsername@gmail.com",
                "password": "password"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this username already exists"} 

def test_repeated_email():
    with db_session:
        User(
            username = "testEmail",
            email = "testEmail@gmail.com",
            password = "password",
            is_validated = False
            )
    response = client.post(
        '/signup',
        json = {
                "username": "testEmail_2",
                "email": "testEmail@gmail.com",
                "password": "password"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this email already exists"} 

def test_bad_password():
    response = client.post(
        '/signup',
        json = {
                "username": "testPassword",
                "email": "testPassword@gmail.com",
                "password": "pass"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "The password must have a minimum of 8 characters"} 





