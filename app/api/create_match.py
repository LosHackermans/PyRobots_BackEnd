from fastapi import FastAPI, Request
import jwt
from pydantic import BaseModel
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import *

router = APIRouter()


# body que me deberian pasar en el request
class BodyMatch(BaseModel):
    name: str
    number_of_rounds: int
    number_of_games: int
    min_players: int
    max_players: int
    password: str
    id_robot: int





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
            curent_user = get_user(request.headers)
            if curent_user == None:     # no existe el usuario en la bd o no hay header
                return {'error': 'Invalid X-Token header'}
            match = Match(name=body.name, min_players=body.min_players,
                          max_players=body.max_players, number_rounds=body.number_of_rounds,
                          number_games=body.number_of_games, is_joinable=True,
                          is_finished =False, password=body.password,
                          user=curent_user)
                          
            Robot_in_match(robot=Robot[body.id_robot], games_won=0,
                            games_draw=0, match=Match[match.id])
            commit()
            return {'match_id': match.id}
    
