from .main import *
from fastapi.testclient import TestClient
import jwt

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
def test_read_main():
    response = client.get(
        "/robots",
        headers={"authorization": "Bearer " + encoded}
    )
    assert response.status_code == 200
    assert response.json() == {"robots":[{'id': 3, 'name': 'example3'}, {'id': 6, 'name': 'example3'}, {'id': 2, 'name': 'example2'},
     {'id': 5, 'name': 'example2'}, {'id': 1, 'name': 'example1'}, {'id': 4, 'name': 'example1'}]}

def test_bad_token_read_main():
    response = client.get(
        "/robots",
        headers={"authorization": "Bearer " + encoded2}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid X-Token header'}

def test_bad_header_read_main():
    response = client.get(
        "/robots",
        headers={"authorization": encoded}
    )
    assert response.status_code == 200
    assert response.json() == {'error': 'Invalid header'}