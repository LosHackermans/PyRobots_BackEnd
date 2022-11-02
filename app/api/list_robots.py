from fastapi import FastAPI, Request
import jwt
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import *

router = APIRouter()


def get_user_robots(user):
    list_of_robots = []
    robots = Robot.select(lambda r: r.user == user).   order_by(
        desc(Robot.name), Robot.id)[:]
    for i in robots:
        list_of_robots.append({"id": i.id, "name": i.name})

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