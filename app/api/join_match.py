from email.headerregistry import ParameterizedMIMEHeader
from functools import partialmethod
from importlib.metadata import requires
from unicodedata import name
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


# NOTE: The BaseModel fails if user not created
class JoinMatchModel(BaseModel): 
    id_match: int # El front puede enviar id? El nombre y demas puede repetirse
    password_match: str
    id_robot: str

    class Config:
        schema_extra = {
            'example': {
                "id_match": 1,
                "password_match": "testPassword",
                "id_robot": 1
            }
        }


@router.post('/join_match')
async def join_match(match: JoinMatchModel):
 
    with db_session:
        # NOTE: For now the password is not required

        current_match = Match.get(id = match.id_match)
        if current_match == None: # Ver si esto puede pasar
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Match does not exist")

        if current_match.is_joinable == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Unable to join match")


        current_robot = Robot.get(id = match.id_robot)
        if current_robot == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Robot does not exist")

        Robot_in_match(robot = current_robot, games_won = 0, games_draw = 0, match = current_match)


        number_of_robots =  current_match.robot_in_matches.count()
        print(number_of_robots)
        if number_of_robots == current_match.max_players:
            current_match.is_joinable = False

    return {'match_id': current_match.id}

