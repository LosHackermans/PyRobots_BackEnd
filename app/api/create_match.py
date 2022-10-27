from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
import base64
from app.api.models import *
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json
from pony.orm import db_session
from fastapi import APIRouter

router = APIRouter()

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

# body que me deberian pasar en el request
class BodyMatch(BaseModel):
    name: str
    number_of_rounds: int
    number_of_games: int
    min_players: int
    max_players: int
    password: str
    id_robot: int


def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    current_user = User.get(email=current_user_info["email"])
    return current_user


@router.post("/create_match")
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
