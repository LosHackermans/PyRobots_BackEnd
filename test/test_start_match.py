from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)




def test_invalid_match():

    response = client.post(
        "/start/345", 345
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'The match does not exist'}

    
def test_not_ready_yet():
    with db_session:
        user_test = User(username = "gatito23", email = "tero23@gmail.com", password = "nuevofamaf256", is_validated = True)
        user_robot =  Robot(name="robot156",script="abc123",user=user_test)
        current_match = Match(name= "resting", min_players= 2,
            max_players= 4, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "prueba22",
            user= user_test)

        Robot_in_match(robot = user_robot, games_won = 0, games_draw = 0, match = current_match)
    
    response = client.post(
        '/start/{current_match.id}', current_match.id)
    
    assert response.status_code == 200
    assert response.json() ==  {"detail": "The match is not ready to start yet"}
    with db_session:
        delete(r for r in Robot if r.name == "robot156")
        delete(r for r in User if r.username == "gatito23")
        delete(r for r in Match if r.name == "resting")





# def test_correct_number_of_players():
#     with db_session:
#         user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
#         Robot(name="robot15689",script="abc",user=user_test)
#         current_match = Match(name= "testMatch", min_players= 2,
#             max_players= 2, number_rounds= 100, 
#             number_games= 100, is_joinable=True,
#             password= "testPassword",
#             user= user_test)

#         user_test_2 = User(username = "testUser2", email = "testUser2@gmail.com", password = "testUser2", is_validated = True)
#         robot_test_2 = Robot(name="robot2",script="abc",user=user_test_2)

    
#     response = client.post(
#         '/start/{current_match.id}')
    
#     assert response.status_code == 200
#     assert response.json() == {"detail": "The match has started"}
#     with db_session:
#         delete(r for r in Robot if r.name == "robot1")
#         delete(r for r in Robot if r.name == "robot2")
#         delete(r for r in User if r.username == "testUser")
#         delete(r for r in User if r.username == "testUser2")
#         delete(r for r in Match if r.name == "testMatch")
