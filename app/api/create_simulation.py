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
    cant_rondas: int

    class Config:
        schema_extra = {
            'example': {
                "robots": [1,2,3],
                "cant_rondas": 200,
            }
        }



@router.post("/simulation")
async def create_simulation(simu: simulationModel):
    if simu.cant_rondas <= 0 or simu.cant_rondas > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="error")
    else:
        positions = {
            "rondas": 
            [
            {
                1: {"x": 200 , "y": 200 , "vida": 50},
                2: {"x": 400 , "y": 400 , "vida": 30}
            }
            ]
        }

        return positions
