from fastapi.testclient import TestClient
from app.main import app
from pony.orm import db_session
from app.api.models import *
client = TestClient(app)



#test
# def test_valid_example():
#     with db_session:
#         user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
#         Robot(name="robot1",script="abc",user=user_test)
#         current_match = Match(name= "testMatch", min_players= 2,
#             max_players= 4, number_rounds= 100, 
#             number_games= 100, is_joinable=True,
#             password= "testPassword",
#             user= user_test)
#         user_test_2 = User(username = "testUser2", email = "testUser2@gmail.com", password = "testUser2", is_validated = True)
#         robot_test_2 = Robot(name="robot2",script="abc",user=user_test_2)
    
    
#     response = client.post(
#         '/join_match',
#         json = {
#                 "id_match": current_match.id,
#                 "password_match": " ", # NOTE: Password not implemented yet
#                 "id_robot": robot_test_2.id 
#             })
#     assert response.status_code == 200
#     assert response.json() == {"message": "User joined successfully"}
#     with db_session:
#         delete(r for r in Robot if r.name == "robot1")
#         delete(r for r in Robot if r.name == "robot2")
#         delete(r for r in User if r.username == "testUser")
#         delete(r for r in User if r.username == "testUser2")
#         delete(r for r in Match if r.name == "testMatch")

def test_match_is_not_joinable():
    with db_session:
        user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
        Robot(name="robot1",script="abc",user=user_test)
        current_match = Match(name= "testMatch", min_players= 2,
            max_players= 4, number_rounds= 100, 
            number_games= 100, is_joinable=False,
            password= "testPassword",
            user= user_test)
        user_test_2 = User(username = "testUser2", email = "testUser2@gmail.com", password = "testUser2", is_validated = True)
        robot_test_2 = Robot(name="robot2",script="abc",user=user_test_2)
    
    
    response = client.post(
        '/join_match',
        json = {
                "id_match": current_match.id,
                "password_match": " ", # NOTE: Password not implemented yet
                "id_robot": robot_test_2.id 
            })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Unable to join match'}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in Robot if r.name == "robot2")
        delete(r for r in User if r.username == "testUser")
        delete(r for r in User if r.username == "testUser2")
        delete(r for r in Match if r.name == "testMatch")

def test_match_does_not_exist():
    with db_session:
        user_test_2 = User(username = "testUser2", email = "testUser2@gmail.com", password = "testUser2", is_validated = True)
        robot_test_2 = Robot(name="robot2",script="abc",user=user_test_2)
    
    
    response = client.post(
        '/join_match',
        json = {
                "id_match": 100,
                "password_match": " ", # NOTE: Password not implemented yet
                "id_robot": robot_test_2.id 
            })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Match does not exist'}
    with db_session:
        delete(r for r in Robot if r.name == "robot2")
        delete(r for r in User if r.username == "testUser2")

def test_robot_does_not():
    with db_session:
        user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
        Robot(name="robot1",script="abc",user=user_test)
        current_match = Match(name= "testMatch", min_players= 2,
            max_players= 4, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)
    
    
    response = client.post(
        '/join_match',
        json = {
                "id_match": current_match.id,
                "password_match": " ", # NOTE: Password not implemented yet
                "id_robot": 100
            })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Robot does not exist'}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in User if r.username == "testUser")
        delete(r for r in Match if r.name == "testMatch")

# def test_exceed_maximum_players():
#     with db_session:
#         user_test = User(username = "testUser", email = "testUser@gmail.com", password = "testUser", is_validated = True)
#         Robot(name="robot1",script="abc",user=user_test)
#         current_match = Match(name= "testMatch", min_players= 2,
#             max_players= 2, number_rounds= 100, 
#             number_games= 100, is_joinable=True,
#             password= "testPassword",
#             user= user_test)

#         user_test_2 = User(username = "testUser2", email = "testUser2@gmail.com", password = "testUser2", is_validated = True)
#         robot_test_2 = Robot(name="robot2",script="abc",user=user_test_2)

    
#     response = client.post(
#         '/join_match',
#         json = {
#                 "id_match": current_match.id,
#                 "password_match": " ", # NOTE: Password not implemented yet
#                 "id_robot": robot_test_2.id
#             })
    
#     assert response.status_code == 200
#     assert response.json() == {"message": "User joined successfully"}
#     with db_session:
#         delete(r for r in Robot if r.name == "robot1")
#         delete(r for r in Robot if r.name == "robot2")
#         delete(r for r in User if r.username == "testUser")
#         delete(r for r in User if r.username == "testUser2")
#         delete(r for r in Match if r.name == "testMatch")



