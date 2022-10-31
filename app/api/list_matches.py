from fastapi import FastAPI, Request
import jwt
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter

router = APIRouter()

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800


def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    current_user = User.get(email=current_user_info["email"])
    return current_user


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
        token = request.headers.get("authorization")
        if token[0:7] != "Bearer ":
            return {'error': 'Invalid header'}
        else:
            token = token[7:]
        curent_user = get_current_user(token)
        if curent_user == None:     # no existe el usuario en la bd
            return {'error': 'Invalid X-Token header'}
        else:
            User_Games,Games_To_Join,Games_already_join = get_matchs(curent_user)
            return {'User_Games': User_Games,
             "Games_To_Join": Games_To_Join,
             "Games_already_join":Games_already_join}
