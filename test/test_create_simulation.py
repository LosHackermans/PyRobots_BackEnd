from fastapi.testclient import TestClient
from app.main import *
import jwt
from pony.orm import db_session
from app.api.models import *

client = TestClient(app)

def test_create_simulation_over_200():
    response = client.post(
        "/simulation",
        json ={"robots": [1,2,3], "rounds": 201}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "error"}



def test_create_simulation_equal_0():
    response = client.post(
        "/simulation",
        json ={"robots": [1,2,3], "rounds": 0}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "error"}



def test_create_raw_simulation():
    response = client.post(
        "/simulation",
        json ={"robots": [1,2,3], "rounds": 100}
    )

    assert response.status_code == 200
    #assert response.json() == 
