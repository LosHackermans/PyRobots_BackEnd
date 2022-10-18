import email
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
import base64
from models import *
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json
from pony.orm import db_session

# TODO: put some of this in .env file
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800
FRONTEND_URL = "http://localhost:3001"




# body que me deberian pasar en el request


class Body(BaseModel):
    name: str
    #avatar: str        #aun no acepta png
    script: str


origins = {
    "http://localhost",
    FRONTEND_URL,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def png_to_b64(ph):  
    if ph == None:
        return None
    else:
        with open(ph, "rb") as image2string: 
            converted_string = base64.b64encode(image2string.read())
        return converted_string

def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    current_user = User.get(email=current_user_info["email"])
    return current_user


@app.post("/upload_robot")
async def user_creatematch(body: Body, request: Request):
    with db_session:
        token = request.headers.get("authorization")
        print(request.headers)
        if token is None or token[0:7] != "Bearer ":
            return {'error': 'Invalid header'}
        else:
            token = token[7:]
        curent_user = get_current_user(token)
        if curent_user == None:     # no existe el usuario en la bd
            return {'error': 'Invalid X-Token header'}
        #ph = png_to_b64(body.avatar)       #aun no acepta png
        robot = Robot(name=body.name, script=body.script,
                      user=curent_user)
        commit()
        if robot.id != None:
            return {'detail': "Robot created"}
        else:
            return {'error': 'Create robot failed'}

 
class LoginItem(BaseModel):
    email: str
    password: str
 
 
@app.get("/")
def read_root():
    return {"Bienvenido de nuevo!!!"}
 
 
 
@app.post("/login")
async def login_user(login_item: LoginItem):
    data = jsonable_encoder(login_item)
    with db_session:
        if User.exists(email = data["email"]):
            currentUser = User.get(lambda u: u.email==data["email"])
            if currentUser.password == data["password"]:
                encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                return {'token': encoded_jwt}
            else:
                return  {'error': ' incorrect Password'}
        elif not(User.exists(email = data["email"])):
            return {'error': 'User not exist'}
        else:
            return {'error': 'Login failed'}


