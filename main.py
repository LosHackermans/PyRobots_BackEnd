from re import A
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import Union
from fastapi import FastAPI, Request
from sqlalchemy import true

# Se importa la base de datos
from models import *

# TODO: put some of this in .env file
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800
FRONTEND_URL = "http://localhost:3001"

app = FastAPI()


# lo que deberia pasarme
test_user = {
    "name": "example",
    "number_of_rounds": 200,
    "number_of_games": 100,
    "min_players": 2,
    "max_players": 4,
    "id_robot": 3,
    "token": "abc"
}

# body que me deberian pasar en el request
class Body(BaseModel):
    name: str
    number_of_rounds: int
    number_of_games: int
    min_players: int
    max_players: int
    id_robot: int


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


def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithm=ALGORITHM)
    current_user = User.select(lambda u: u.email == current_user_info["email"])
    #current_user = User.get(email = current_user_info["email"])
    return current_user


@app.get("/")
def read_root():
    return {"Bienvenido de nuevo!!!"}


@app.post("/create_match")
async def user_creatematch(body: Body, request: Request):
    token = request.headers.get['Bearer']
    curent_user = get_current_user(token)
    if body.number_of_rounds > 10000 or body.number_of_rounds < 0:
        return {'error': 'number of rounds invalid'}
    elif body.number_of_games > 200 or body.number_of_games < 0:
        return {'error': 'number of games invalid'}
    elif body.max_players < body.min_players or body.max_players > 4 or body.min_players < 2:
        return {'error': 'number of players invalid'}
    else:
        with db_session:
            m1 = Match(name=body.name, min_players=body.min_players,
                       max_players=body.max_players, number_rounds=body.number_of_rounds,
                       number_games=body.number_of_games, joinable=true,
                       user=curent_user)
            m1.robot_in_matches.add(Robot[body.id_robot])
            commit()
            if m1.id != None:
                return {m1.id: int}
            else:
                return {'error': 'Create match failed'}
