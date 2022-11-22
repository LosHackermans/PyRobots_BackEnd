from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
dummy_user = {
    "email": "famaf15@gmail.com",
    "password": "nuevofamaf"
}
dummy_user2 = {
    "email": "famaf16@gmail.com",
    "password": "nuevofamaf"
}
encoded_jwt = jwt.encode(dummy_user, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")

encoded_jwt2 = jwt.encode(dummy_user2, SECRET_KEY, algorithm=ALGORITHM)
encoded2 = encoded_jwt2.decode("utf-8")


def test_invalid_header():

    response = client.post(
        "/abandon/{current_match.id}",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}


# def test_invalid_match():
#     with db_session:
#         user_test = User(username = "pedro38", email = "famaf15@gmail.com", password = "nuevofamaf", is_validated = True)
#         match_id = 23
    
#     response = client.post(
#         "/abandon/{match_id}",
#         headers={"authorization": "Bearer " + encoded})

#     assert response.status_code == 200
#     assert response.json() == {'error': 'The match does not exist'}
#     with db_session:
#         delete(r for r in User if r.username == "pedro38")


    
def test_remove_successfull():
    with db_session:
        user_test = User(username = "pedro35", email = "famaf15@gmail.com", password = "nuevofamaf", is_validated = True)
        #user_test2 = User(username = "pedro22", email = "famaf16@gmail.com", password = "nuevofamaf2", is_validated = True)
        user_robot = Robot(name="robot1",script="abc",user=user_test)
        #user_robot2 = Robot(name="robot2",script="abcd",user=user_test2)
        current_match = Match(name= "testMatch", min_players= 2,
            max_players= 4, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)
        
        Robot_in_match(robot = user_robot, games_won = 0, games_draw = 0, match = current_match)
        #Robot_in_match(robot = user_robot2, games_won = 0, games_draw = 0, match = current_match)
        
    response = client.post(
        '/abandon/{current_match.id}',
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User remove successful from the match"}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in Robot if r.name == "robot2")
        delete(r for r in User if r.username == "pedro35")
        delete(r for r in User if r.username == "pedro22")
        delete(r for r in Match if r.name == "testMatch")