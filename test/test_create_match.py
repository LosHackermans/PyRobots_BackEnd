from fastapi.testclient import TestClient
from app.main import app
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

