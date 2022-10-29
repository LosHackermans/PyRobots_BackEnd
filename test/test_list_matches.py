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


def test_valid_example():
    with db_session:
        User(username="ej", email="pepito@gmail.com",
             password="abc", is_validated=True)
        Match(name="match1", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User[1])
        Match(name="match2", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(username="ej"))
        Match(name="match3", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(username="ej"))
        id1 = (Match.get(name="match1")).id
        id2 = (Match.get(name="match2")).id
        id3 = (Match.get(name="match3")).id
    response = client.get(
        "/matches",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {"PartidasDeUsuario": [{'id': id1, 'name': 'match1'}],
                               "PartidasParaUnirse": [{'id': id3, 'name': 'match3'}, 
                               {'id': id2, 'name': 'match2'}]}
    with db_session:
        delete(m for m in Match if m.name == "match1")
        delete(m for m in Match if m.name == "match2")
        delete(m for m in Match if m.name == "match3")
        delete(u for u in User if u.username == "ej")


def test_invalid_token():
    response = client.get(
        "/matches",
        headers={"authorization": "Bearer " + encoded2}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}


def test_invalid_header():
    response = client.get(
        "/matches",
        headers={"authorization": encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid header'}
