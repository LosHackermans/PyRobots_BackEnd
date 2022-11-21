from fastapi import FastAPI, Request
import jwt
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import *

router = APIRouter()

def get_robot_statistics(id_robot):
    robot_games = select(e for e in Robot_in_match if (e.robot == id_robot))

    games_draw = 0
    games_won = 0
    games_played = 0

    for i in robot_games:
        if i.match.is_finished == True:
            games_won += i.games_won
            games_draw += i.games_draw
            games_played += 1


    return games_won, games_draw, games_played

def get_user_robots(user):
    list_of_robots = []
    robots = Robot.select(lambda r: r.user == user).   order_by(
        desc(Robot.name), Robot.id)[:]
    for i in robots:
        games_won, games_draw, games_played = get_robot_statistics(i)
        list_of_robots.append({"id": i.id, "name": i.name, "avatar": i.avatar, "games_won": games_won, "games_draw": games_draw, "games_played": games_played})

    return list_of_robots


@router.get("/robots")
async def list_robots(request: Request):
    with db_session:
        curent_user = get_user(request.headers)
        if curent_user == None:     # no existe el usuario en la bd o no hay header
            return {'error': 'Invalid X-Token header'}
        else:
            user_robots = get_user_robots(curent_user)
            return {'robots':user_robots}