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
dummy_user2 = {
    "email": "famaf02@gmail.com",
    "password": "nuevofamaf"
}
encoded_jwt = jwt.encode(dummy_user, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")

encoded_jwt2 = jwt.encode(dummy_user2, SECRET_KEY, algorithm=ALGORITHM)
encoded2 = encoded_jwt2.decode("utf-8")


# test create match
def test_read_main3():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Bienvenido de nuevo!!!"}


def test_create_item3():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "example", "number_of_rounds": 200, "number_of_games": 100, 
        "min_players": 2, "max_players": 4, "pasword": "add","id_robot": 1}
    )
    assert response.status_code == 200
    
def test_bad_create_item3():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json = {"name": "example", "number_of_rounds": 200, "number_of_games": 500, 
        "min_players": 2, "max_players": 4,"pasword": "add", "id_robot": 1}
    )
    assert response.status_code == 200    
    assert response.json() == {'error': 'number of games invalid'}

def test_read_item_bad_token3():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded2},
        json = {"name": "example", "number_of_rounds": 200, "number_of_games": 100, 
        "min_players": 2, "max_players": 4, "pasword": "add", "id_robot": 1}
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

