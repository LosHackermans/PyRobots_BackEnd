from fastapi import FastAPI
import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800


dummy_user = {
    "username": "famaf01",
    "password": "nuevofamaf",
}


app = FastAPI()


class LoginItem(BaseModel):
    username: str
    password: str

    
@app.get("/")
def read_root():
    return {"Bienvenido de nuevo"}


@app.post("/login")
async def login_user(login_item: LoginItem):
    data = jsonable_encoder(login_item)
    if dummy_user['username'] == data['username'] and dummy_user['username'] == data['username']:
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return {'token': encoded_jwt }
    else:
        return {'message': 'Login failed'}