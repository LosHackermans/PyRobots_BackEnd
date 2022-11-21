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

    for match in matchs:
        if not match.is_finished:
            if match.user == user:
                User_Games.append({"id": match.id, "name": match.name})
            else:
                esta_unido = False
                for robot_in_match in match.robot_in_matches:
                    for robot in user.robots:
                        if robot_in_match.robot == robot and match.user != user:
                            Games_already_join.append(
                                {"id": match.id, "name": match.name})
                            esta_unido = True
                if not esta_unido and match.is_joinable:
                    Games_To_Join.append({"id": match.id, "name": match.name})
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
