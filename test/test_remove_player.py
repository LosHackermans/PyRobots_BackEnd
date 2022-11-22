from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
dummy_user = {
    "email": "guerra15@gmail.com",
    "password": "le_nuevofamaf"
}
dummy_user2 = {
    "email": "tumbar16@gmail.com",
    "password": "il_nuevofamaf2"
}
encoded_jwt = jwt.encode(dummy_user, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")

encoded_jwt2 = jwt.encode(dummy_user2, SECRET_KEY, algorithm=ALGORITHM)
encoded2 = encoded_jwt2.decode("utf-8")


# def test_invalid_header():

#     response = client.post(
#         "/abandon/{current_match.id}",
#         headers={"authorization": "Bearer " + encoded}
#     )
#     assert response.status_code == 200
#     assert response.json() == {'error': 'Invalid X-Token header'}


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


    
# def test_remove_successfull():
#     with db_session:
#         testeado_user = User(username = "benicio35", email = "guerra15@gmail.com", password = "le_nuevofamaf", is_validated = True)
#         perrito_mal = User(username = "suero22", email = "tumbar16@gmail.com", password = "il_nuevofamaf2", is_validated = True)
#         el_robot = Robot(name="robot1330",script="ueurywirw",user=testeado_user)
#         tu_robot = Robot(name="robot2809",script="ofisp4323",user=perrito_mal)
#         current_match = Match(name= "not_this", min_players= 2,
#             max_players= 4, number_rounds= 100, 
#             number_games= 100, is_joinable=True,
#             password= "testPassword",
#             user= testeado_user)
        
#         Robot_in_match(robot = el_robot, games_won = 0, games_draw = 0, match = current_match)
#         Robot_in_match(robot = tu_robot, games_won = 0, games_draw = 0, match = current_match)
        
#     response = client.post(
#         '/abandon/{current_match.id}',
#         headers={"authorization": "Bearer " + encoded}
#     )
#     assert response.status_code == 200
#     assert response.json() == {"detail": "User remove successful from the match"}
#     with db_session:
#         delete(r for r in Robot if r.name == "robot1330")
#         delete(r for r in Robot if r.name == "robot2809")
#         delete(r for r in User if r.username == "benicio35")
#         delete(r for r in User if r.username == "suero22")
#         delete(r for r in Match if r.name == "not_this")