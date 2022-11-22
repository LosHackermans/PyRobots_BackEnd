from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *
from app.api.lobby import *
from robots.Partida import Partida


client = TestClient(app)


def test_get_room():
    with db_session:
        user_test = User(username = "tenso789", email = "prensa34@gmail.com",
             password = "trueque358", is_validated = True)

        user_robot =Robot(name="libert1220", script="abc3453", user=User.get(email="prensa34@gmail.com"))

        current_match = Match(name= "is_testMatch", min_players= 2,
            max_players= 4, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)

        user_robot_in = Robot_in_match(robot = user_robot, games_won =0, games_draw =0, match = current_match)

    assert get_room(current_match.id) == {"Creator": {"Owner": user_test.username,
                                 "Robot_name": user_robot.name}, "Players": []}
    with db_session:
        delete(u for u in User if u.email == "prensa34@gmail.com")
        delete(r for r in Robot if r.name == "libert1220")
        delete(r for r in Match if r.name == "is_testMatch")

