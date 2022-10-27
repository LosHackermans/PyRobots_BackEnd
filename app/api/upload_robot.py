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

class Body(BaseModel):
    name: str
    # avatar: str        #aun no acepta png
    script: str


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

@router.post("/upload_robot")
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
