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



def test_invalid_match():

    response = client.post(
        "/start/abhsbakj"
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'The match does not exist'}

    
def test_not_ready_yet():
    with db_session:
        user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
        Robot(name="robot1",script="abc",user=user_test)
        current_match = Match(name= "testMatch", min_players= 2,
            max_players= 2, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)

    
    response = client.post(
        '/start/{current_match.id}')
    
    assert response.status_code == 200
    assert response.json() ==  {"detail": "The match is not ready to start yet"}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in User if r.username == "testUser")
        delete(r for r in Match if r.name == "testMatch")


def test_correct_number_of_players():
    with db_session:
        user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
        Robot(name="robot1",script="abc",user=user_test)
        current_match = Match(name= "testMatch", min_players= 2,
            max_players= 2, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)

        user_test_2 = User(username = "testUser2", email = "testUser2@gmail.com", password = "testUser2", is_validated = True)
        robot_test_2 = Robot(name="robot2",script="abc",user=user_test_2)

    
    response = client.post(
        '/start/{current_match.id}')
    
    assert response.status_code == 200
    assert response.json() == {"detail": "The match has started"}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in Robot if r.name == "robot2")
        delete(r for r in User if r.username == "testUser")
        delete(r for r in User if r.username == "testUser2")
        delete(r for r in Match if r.name == "testMatch")
