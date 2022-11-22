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

    
# def test_not_ready_yet():
#     with db_session:
#         user_test = User(username = "gatito23", email = "tero23@gmail.com", password = "nuevofamaf256", is_validated = True)
#         user_robot =  Robot(name="robot156",script="abc123",user=user_test)
#         current_match = Match(name= "resting", min_players= 2,
#             max_players= 4, number_rounds= 100, 
#             number_games= 100, is_joinable=True,
#             password= "prueba22",
#             user= user_test)

#         Robot_in_match(robot = user_robot, games_won = 0, games_draw = 0, match = current_match)
    
#     response = client.post(
#         '/start/{current_match.id}', current_match.id)
    
#     assert response.status_code == 200
#     assert response.json() ==  {"detail": "The match is not ready to start yet"}
#     with db_session:
#         delete(r for r in Robot if r.name == "robot156")
#         delete(r for r in User if r.username == "gatito23")
#         delete(r for r in Match if r.name == "resting")





# def test_correct_number_of_players():
#     with db_session:
#         new_user_t = User(username = "fair_user", email = "juego34@gmail.com", password = "serioleta", is_validated = True)
#         Robot(name="robot15689",script="abcakjhdka",user=new_user_t)
#         le_nuevo_m = Match(name= "new_m_t", min_players= 2,
#             max_players= 2, number_rounds= 100, 
#             number_games= 100, is_joinable=True,
#             password= "testPassword",
#             user= new_user_t)

#         never_user2 = User(username = "never_user", email = "nvu@gmail.com", password = "neveruser2", is_validated = True)
#         never_bot2 = Robot(name="no_bot2",script="abciuytr",user=never_user2)

    
#     response = client.post(
#         '/start/{le_nuevo_m.id}')
    
#     assert response.status_code == 200
#     assert response.json() == {"detail": "The match has started"}
#     with db_session:
#         delete(r for r in Robot if r.name == "robot15689")
#         delete(r for r in Robot if r.name == "no_bot2")
#         delete(r for r in User if r.username == "fair_user")
#         delete(r for r in User if r.username == "never_user")
#         delete(r for r in Match if r.name == "new_m_t")
