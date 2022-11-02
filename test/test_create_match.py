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


# test create match
def test_create_match():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)
        Robot(name="robot", script="abc", user=User.get(email = "famaf01@gmail.com"))
        id = (Robot.get(name="robot", user=User.get(email = "famaf01@gmail.com"))).id
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "example", "number_of_rounds": 200, "number_of_games": 100,
              "min_players": 2, "max_players": 4, "password": "add", "id_robot": id}
    )
    assert response.status_code == 200
    with db_session:
        m = Match.get(user = User.get(email = "famaf01@gmail.com"))
    assert response.json() == {'match_id': m.id}
    with db_session:
        delete(r for r in Robot if r.name == "robot" and r.user == User.get(email = "famaf01@gmail.com"))
        delete(m for m in Match if m.name == "example" and m.user == User.get(email = "famaf01@gmail.com"))
        delete (u for u in User if u.email == "famaf01@gmail.com")

def test_invalid_games():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "example", "number_of_rounds": 200, "number_of_games": 500,
              "min_players": 2, "max_players": 4, "password": "add", "id_robot": 1}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'number of games invalid'}

def test_invalid_players():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "example", "number_of_rounds": 200, "number_of_games": 100,
        "min_players": 2, "max_players": 10, "password": "add", "id_robot": 1}
        )
    assert response.status_code == 200
    assert response.json() == {'error': 'number of players invalid'}

def test_invalid_rounds():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded},
        json={"name": "example", "number_of_rounds": -200, "number_of_games": 100,
        "min_players": 2, "max_players": 4, "password": "add", "id_robot": 1}
        )
    assert response.status_code == 200
    assert response.json() == {'error': 'number of rounds invalid'}


def test_invalid_token():
    response = client.post(
        "/create_match",
        headers={"authorization": "Bearer " + encoded2},
        json={"name": "example", "number_of_rounds": 200, "number_of_games": 100,
              "min_players": 2, "max_players": 4, "password": "add", "id_robot": 1}
    )
    assert response.status_code == 200
    assert response.json() == {"error": "Invalid X-Token header"}


def test_invalid_header():
    response = client.post(
        "/create_match",
        headers={"authorization": encoded},
        json={"name": "example", "number_of_rounds": 200, "number_of_games": 100,
              "min_players": 2, "max_players": 4, "password": "add", "id_robot": 1}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}
