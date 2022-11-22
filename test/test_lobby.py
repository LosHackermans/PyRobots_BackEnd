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
        user_test = User(username = "pedro789", email = "famaf295@gmail.com",
             password = "nuevofamaf358", is_validated = True)
        #user_test2 = User(username="ej", email="pepito@gmail.com",
        #         password="abc", is_validated=True)

        user_robot =Robot(name="robot1220", script="abc3453", user=User.get(email="famaf295@gmail.com"))
        #user_robot2 = Robot(name="robot257", script="abcd", user=User.get(email="pepito@gmail.com"))

        current_match = Match(name= "is_testMatch", min_players= 2,
            max_players= 4, number_rounds= 100, 
            number_games= 100, is_joinable=True,
            password= "testPassword",
            user= user_test)

        user_robot_in = Robot_in_match(robot = user_robot, games_won =0, games_draw =0, match = current_match)

    assert get_room(current_match.id) == {"Creator": {"Owner": user_test.username,
                                 "Robot_name": user_robot.name}, "Players": []}
    with db_session:
        #delete(u for u in User if u.email == "pepito@gmail.com")
        delete(u for u in User if u.email == "famaf295@gmail.com")
        delete(r for r in Robot if r.name == "robot1220")
        #delete(r for r in Robot if r.name == "robot257")
        delete(r for r in Match if r.name == "is_testMatch")

