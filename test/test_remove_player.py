from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)


def test_invalid_header():
    response = client.post(
        "/abandon/{match_id}",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}


def test_invalid_match():

    response = client.post(
        "/abandon/abhsbakj",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'The match does not exist'}


    
def test_remove_successfull():
    
    user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
    Robot(name="robot1",script="abc",user=user_test)
    current_match = Match(name= "testMatch", min_players= 2,
            max_players= 2, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)

    response = client.post(
        "/abandon/{current_match.id}",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User remove successful from the match"}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in User if r.username == "testUser")
        delete(r for r in Match if r.name == "testMatch")