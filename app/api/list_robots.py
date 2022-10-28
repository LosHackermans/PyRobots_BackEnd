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

def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    current_user = User.get(email=current_user_info["email"])
    return current_user

def get_user_robots(User):
    list_of_robots = []
    robots = Robot.select(lambda r: r.user == User).   order_by(
        desc(Robot.name), Robot.id)[:]
    for i in robots:
        list_of_robots.append({"id": i.id, "name": i.name})

    return list_of_robots


@router.get("/robots")
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
            return {'robots':user_robots}