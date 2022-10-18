from fastapi.testclient import TestClient
from .main import *
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


#test list robots
def test_read_main4():
    response = client.get(
        "/robots",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {"robots":[{'id': 3, 'name': 'example3'}, {'id': 6, 'name': 'example3'}, {'id': 2, 'name': 'example2'},
     {'id': 5, 'name': 'example2'}, {'id': 1, 'name': 'example1'}, {'id': 4, 'name': 'example1'}]}

def test_bad_token_read_main4():
    response = client.get(
        "/robots",
        headers={"authorization": "Bearer " + encoded2}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}

def test_bad_header_read_main4():
    response = client.get(
        "/robots",
        headers={"authorization": encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid header'}

# test create user
def test_create_user():
    response = client.post(
        '/create_user',
        json = {
                "username": "Juan5",
                "email": "juanpereez@gmail.co5",
                "password": "password"
                #"passwordRepeated": "password"
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
        '/create_user',
        json = {
                "username": "testUser",
                "email": "testUsername@gmail.com",
                "password": "password",
                "passwordRepeated": "password"
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
        '/create_user',
        json = {
                "username": "testEmail_2",
                "email": "testEmail@gmail.com",
                "password": "password",
                "passwordRepeated": "password"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this email already exists"} 

def test_bad_password():
    response = client.post(
        '/create_user',
        json = {
                "username": "testPassword",
                "email": "testPassword@gmail.com",
                "password": "pass",
                "passwordRepeated": "pass"
            })
    assert response.status_code == 400
    assert response.json() == {"detail": "The password must have a minimum of 8 characters"} 

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

# test create match

def test_create_item3():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "example", "number_of_rounds": 200, "number_of_games": 100, 
        "min_players": 2, "max_players": 4, "password": "add","id_robot": 1}
    )
    assert response.status_code == 200
    
def test_bad_create_item3():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "example", "number_of_rounds": 200, "number_of_games": 500, 
        "min_players": 2, "max_players": 4,"password": "add", "id_robot": 1}
    )
    assert response.status_code == 200    
    assert response.json() == {'error': 'number of games invalid'}

def test_read_item_bad_token3():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded2},
        json = {"name": "example", "number_of_rounds": 200, "number_of_games": 100, 
        "min_players": 2, "max_players": 4, "password": "add", "id_robot": 1}
    )
    assert response.status_code == 200
    assert response.json() == {"error": "Invalid X-Token header"}

# necesario para correr los test (hecho en consola)
# with db_session:
#    User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)




#test upload robot
def test_read_main():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "example", "script": "acd"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail':"Robot created"}

def test_bad_create_item():
    response = client.post(
        "/upload_robot",
        headers={"authorization": "Bearer " + encoded2},
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
