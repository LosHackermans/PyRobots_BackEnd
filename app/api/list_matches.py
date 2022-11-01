from fastapi import FastAPI, Request
import jwt
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import *

router = APIRouter()


def get_matchs(user):
    User_Games = []
    Games_To_Join = []
    Games_already_join = []
    matchs = Match.select() .   order_by(
        desc(Match.name), Match.id)[:]
    
    for i in matchs:
        if i.is_joinable:   # si la partida esta llena, o ya comenzo esta variable es false
        
            if i.user == user:
                User_Games.append({"id": i.id, "name": i.name})
            else:
                esta_unido = False
                for j in i.robot_in_matches:
                    for h in user.robots:
                        if j.robot == h and i.user != user:
                            Games_already_join.append({"id": i.id, "name": i.name})
                            esta_unido = True
                if not esta_unido:       
                    Games_To_Join.append({"id": i.id, "name": i.name})
    return (User_Games, Games_To_Join, Games_already_join)


@router.get("/matches")
async def list_matches(request: Request):
    with db_session:
        curent_user = get_user(request.headers)
        if curent_user == None:     # no existe el usuario en la bd o no hay header
            return {'error': 'Invalid X-Token header'}
        else:
            User_Games,Games_To_Join,Games_already_join = get_matchs(curent_user)
            return {'User_Games': User_Games,
             "Games_To_Join": Games_To_Join,
             "Games_already_join":Games_already_join}
