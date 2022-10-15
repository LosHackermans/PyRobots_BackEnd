import email
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


################
from typing import Optional
import json
from pony.orm import db_session



#Se importa la base de datos
from models import *

 
# TODO: put some of this in .env file
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800
FRONTEND_URL = "http://localhost:3001"
 
app = FastAPI()

 

# Usuario generico de prueba
dummy_user = {
    "email": "famaf01@gmail.com",
    "password": "nuevofamaf"
}
 
origins = {
    "http://localhost",
    FRONTEND_URL,
}
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
class LoginItem(BaseModel):
    email: str
    password: str
 
 
@app.get("/")
def read_root():
    return {"Bienvenido de nuevo!!!"}
 
 
@db_session() 
@app.post("/login")
async def login_user(login_item: LoginItem):
    data = jsonable_encoder(login_item)
    with db_session:
        if User.exist(email == data['email']):
            currentUser = User.select(lambda u: u.email==data['email'])
            if currentUser.password == data['password']:
                encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                return {'token': encoded_jwt}
            else:
                return  {'error': 'Password incorrecta'}
        elif not(User.exist(email == data['email'])):
            return {'error': 'No existe el usuario'}
        else:
            return {'error': 'Login failed'}



# @app.post("/login")
# async def login_user(login_item: LoginItem):
#     data = jsonable_encoder(login_item)
#     if dummy_user['email'] == data['email'] and dummy_user['password'] == data['password']:
#         encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
#         return {'token': encoded_jwt}
#     else:
#         return {'error': 'Login failed'}
