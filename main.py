from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
import base64
from models import *
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json
from pony.orm import db_session

app = FastAPI()
# TODO: put some of this in .env file
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800
FRONTEND_URL = "http://localhost:3001"


class BodyMatch(BaseModel):
    name: str
    number_of_rounds: int
    number_of_games: int
    min_players: int
    max_players: int
    password: str
    id_robot: int


class signUpModel(BaseModel):
    username: str
    email: str
    password: str
    # avatar: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                "username": "Juan",
                "email": "juanperez@gmail.com",
                "password": "password"
            }
        }


class Body(BaseModel):
    name: str
    # avatar: str        #aun no acepta png
    script: str


origins = {
    "http://localhost",
    FRONTEND_URL,
}


def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithm=ALGORITHM)
    current_user = User.get(email=current_user_info["email"])
    return current_user


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
        if token[0:7] != "Bearer ":
            return {'error': 'Invalid header'}
        else:
            token = token[7:]
        curent_user = get_current_user(token)
        if curent_user == None:     # no existe el usuario en la bd
            return {'error': 'Invalid X-Token header'}
        # ph = png_to_b64(body.avatar)       #aun no acepta png
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


@app.post('/create_user')
async def signup(user: signUpModel):
    with db_session:
        usernameQuery = select(
            e.username for e in User if (e.username == user.username))
        if len(usernameQuery) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this username already exists")
        emailQuery = select(e.email for e in User if (e.email == user.email))
        if len(emailQuery) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exists")
        if len(user.password) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The password must have a minimum of 8 characters")
        # if user.password != user.passwordRepeated:
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            # detail= "Passwords do not match")

        User(
            username=user.username,
            email=user.email,
            password=user.password,
            is_validated=False
        )

    return {"message": "User created successfully"}


def read_root():
    return {"msg": "Bienvenido de nuevo!!!"}


@app.post("/create_match")
async def user_creatematch(body: BodyMatch, request: Request):
    if body.number_of_rounds > 10000 or body.number_of_rounds < 0:
        return {'error': 'number of rounds invalid'}
    elif body.number_of_games > 200 or body.number_of_games < 0:
        return {'error': 'number of games invalid'}
    elif body.max_players < body.min_players or body.max_players > 4 or body.min_players < 2:
        return {'error': 'number of players invalid'}
    else:
        with db_session:
            token = request.headers.get("authorization")
            if token[0:7] != "Bearer ":
                return {'error': 'Invalid header'}
            else:
                token = token[7:]
            curent_user = get_current_user(token)
            if curent_user == None:     # no existe el usuario en la bd
                return {'error': 'Invalid X-Token header'}
            match = Match(name=body.name, min_players=body.min_players,
                          max_players=body.max_players, number_rounds=body.number_of_rounds,
                          number_games=body.number_of_games, is_joinable=True,
                          password=body.password,
                          user=curent_user)
            commit()
            if match.id != None:
                Robot_in_match(robot=Robot[body.id_robot], games_won=0,
                               games_draw=0, match=Match[match.id])
                commit()
                return {'match_id': match.id}
            else:
                return {'error': 'Create match failed'}


@app.post("/login")
async def login_user(login_item: LoginItem):
    data = jsonable_encoder(login_item)
    with db_session:
        if User.exists(email=data["email"]):
            currentUser = User.get(lambda u: u.email == data["email"])
            if currentUser.password == data["password"]:
                encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                return {'token': encoded_jwt}
            else:
                return {'error': ' incorrect Password'}
        elif not(User.exists(email=data["email"])):
            return {'error': 'User not exist'}
        else:
            return {'error': 'Login failed'}


def get_user_robots(User):
    list_of_robots = []
    robots = Robot.select(lambda r: r.user == User).   order_by(
        desc(Robot.name), Robot.id)[:]
    for i in robots:
        list_of_robots.append({"id": i.id, "name": i.name})

    return list_of_robots


@app.get("/robots")
async def list_robots(request: Request):
    with db_session:
        token = request.headers.get("authorization")
        if token[0:7] != "Bearer ":
            return {'error': 'Invalid header'}
        else:
            token = token[7:]
        curent_user = get_current_user(token)
        if curent_user == None:     # no existe el usuario en la bd
            return {'error': 'Invalid X-Token header'}
        else:
            user_robots = get_user_robots(curent_user)
            return {'robots': user_robots}
