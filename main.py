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
            currentUser = User.get(lambda u: u.email==data['email'])
            if currentUser.password == data['password']:
                encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                return {'token': encoded_jwt}
            elif (currentUser.is_validated):
                return {'error': 'You are no validated'}    
            else:
                return  {'error': ' incorrect Password'}
        elif not(User.exist(email == data['email'])):
            return {'error': 'User not exist'}
        else:
            return {'error': 'Login failed'}

