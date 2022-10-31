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
        list_of_robots = simu.robots
        number_of_robots = len(list_of_robots)
        number_of_rounds = simu.rounds
        
        dictionary = {}
        list_of_rounds = []

        for i in range(number_of_rounds):
            for j in range(number_of_robots):
                
                current_robot = list_of_robots[j]
                #######################################
                #Falta obtener robot y sus datos del j-esimo robot
                #Hardcode data
                x_position = 300
                y_position = 450
                robot_life = 50
                #####################################################

                dictionary[j+1] = {"x": x_position, "y": y_position, "life": robot_life}

            list_of_robots.append(dictionary)
            dictionary = {}


        positions = {
            "rounds": list_of_rounds
        }

        return positions
