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
from robots.Juego import Juego

router = APIRouter()


class simulationModel(BaseModel):
    robots: list
    rounds: int

    class Config:
        schema_extra = {
            'example': {
                "robots": [1,2,3],
                "rounds": 200,
            }
        }



@router.post("/simulation")
async def create_simulation(simu: simulationModel):
    if simu.rounds <= 0 or simu.rounds > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="error")
    else:
        with db_session:
            robots_query = Robot.select(lambda r: r.id in simu.robots)
            robots_paths = [robot.script for robot in list(robots_query)]
            game = Juego(robots_paths, simu.rounds, is_simulation = True)
            game.run()
            return game.get_results()
