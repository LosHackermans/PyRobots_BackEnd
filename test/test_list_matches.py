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


def test_valid_example():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com",
             password = "nuevofamaf", is_validated = True)
        User(username="ej", email="pepito@gmail.com",
             password="abc", is_validated=True)
        Match(name="match1", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(email="famaf01@gmail.com"))
        Match(name="match2", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(email="pepito@gmail.com"))
        Match(name="match3", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(email="pepito@gmail.com"))
        id1 = (Match.get(name="match1")).id
        id2 = (Match.get(name="match2")).id
        id3 = (Match.get(name="match3")).id
    response = client.get(
        "/matches",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    #assert response.json() == {"User_Games": [{'id': id1, 'name': 'match1'}],
    #                           "Games_To_Join": [{'id': id3, 'name': 'match3'},
    #                                                  {'id': id2, 'name': 'match2'}],
    #                           "Games_already_join": []}
    with db_session:
        delete(m for m in Match if m.name == "match1")
        delete(m for m in Match if m.name == "match2")
        delete(m for m in Match if m.name == "match3")
        delete(u for u in User if u.email == "pepito@gmail.com")
        delete(u for u in User if u.email == "famaf01@gmail.com")


def test_full_valid_example():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com",
             password = "nuevofamaf", is_validated = True)
        User(username="ej", email="pepito@gmail.com",
             password="abc", is_validated=True)
        Robot(name="robot", script="abc", user=User.get(email="famaf01@gmail.com"))
        Match(name="match1", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(email="famaf01@gmail.com"))
        Match(name="match2", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(email="pepito@gmail.com"))
        Match(name="match3", min_players=2, max_players=4,
              number_rounds=200, number_games=200, is_joinable=True, user=User.get(email="pepito@gmail.com"))
        Robot_in_match(robot=Robot.get(name="robot"),
                       games_won=2, games_draw=2, match= Match.get(name="match2", user=User.get( email="pepito@gmail.com")))
        id1 = (Match.get(name="match1", user=User.get(email="famaf01@gmail.com"))).id
        id2 = (Match.get(name="match2", user=User.get(email="pepito@gmail.com"))).id
        id3 = (Match.get(name="match3", user=User.get(email="pepito@gmail.com"))).id
    response = client.get(
        "/matches",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    #assert response.json() == {"User_Games": [{'id': id1, 'name': 'match1'}],
    #                           "Games_To_Join": [{'id': id3, 'name': 'match3'}],
    #                           "Games_already_join": [{'id': id2, 'name': 'match2'}]}
    with db_session:
        delete(m for m in Match if m.name == "match1")
        delete(m for m in Match if m.name == "match2")
        delete(m for m in Match if m.name == "match3")
        delete(r for r in Robot if r.name == "robot")
        delete(r for r in Robot_in_match if r.games_won == 2)
        delete(u for u in User if u.email == "pepito@gmail.com")
        delete(u for u in User if u.email == "famaf01@gmail.com")


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
    assert response.json() == {'error': 'Invalid X-Token header'}
