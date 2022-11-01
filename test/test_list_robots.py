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


#test
def test_valid_example():
    with db_session:
        User(username = "pedro", email = "famaf01@gmail.com",
             password = "nuevofamaf", is_validated = True)
        Robot(name="robot1",script="abc",user=User.get(email = "famaf01@gmail.com"))
        Robot(name="robot2",script="abc",user=User.get(email = "famaf01@gmail.com"))
        Robot(name="robot3",script="abc",user=User.get(email = "famaf01@gmail.com"))
        Robot(name="robot4",script="abc",user=User.get(email = "famaf01@gmail.com"))
        Robot(name="robot5",script="abc",user=User.get(email = "famaf01@gmail.com"))
        Robot(name="robot6",script="abc",user=User.get(email = "famaf01@gmail.com"))
        id1 = (Robot.get(name="robot1")).id
        id2 = (Robot.get(name="robot2")).id
        id3 = (Robot.get(name="robot3")).id
        id4 = (Robot.get(name="robot4")).id
        id5 = (Robot.get(name="robot5")).id
        id6 = (Robot.get(name="robot6")).id
    response = client.get(
        "/robots",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code ==  200
    assert response.json() == {"robots":[{'id': id6, 'name': 'robot6'}, 
    {'id': id5, 'name': 'robot5'}, {'id': id4, 'name': 'robot4'},
    {'id': id3, 'name': 'robot3'}, {'id': id2, 'name': 'robot2'}, {'id': id1, 'name': 'robot1'}]}
    with db_session:
        delete(r for r in Robot if r.name == "robot1")
        delete(r for r in Robot if r.name == "robot2")
        delete(r for r in Robot if r.name == "robot3")
        delete(r for r in Robot if r.name == "robot4")
        delete(r for r in Robot if r.name == "robot5")
        delete(r for r in Robot if r.name == "robot6")
        delete (u for u in User if u.email == "famaf01@gmail.com")


def test_invalid_token():
    response = client.get(
        "/robots",
        headers={"authorization": "Bearer " + encoded2}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}

def test_invalid_header():
    response = client.get(
        "/robots",
        headers={"authorization": encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}