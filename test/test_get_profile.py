from fastapi.testclient import TestClient
from app.main import app
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
dummy_user = {
    "email": "guit@gmail.com",
    "password": "tusergio345"
}


encoded_jwt = jwt.encode(dummy_user, SECRET_KEY, algorithm=ALGORITHM)
encoded = encoded_jwt.decode("utf-8")




def test_invalid_header():
    
    response = client.get(
        "/profile",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}


def test_get_profile_data():

    with db_session:
        User(username = "sergio45", email = "guit@gmail.com", password = "tusergio345", avatar = "", is_validated = True)
    
    response = client.get(
        "/profile" ,
        headers={"authorization": "Bearer " + encoded}
    )

    data_name = {
            "username": "sergio45",
            "email": "guit@gmail.com",
            "avatar":  "" #puede ser Vacio
        }
    assert response.status_code == 200
    assert response.json() == data_name

    with db_session():
        delete(r for r in User if r.username == "sergio45")