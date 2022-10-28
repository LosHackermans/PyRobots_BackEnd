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
async def create_simulation(param: simulationModel):
