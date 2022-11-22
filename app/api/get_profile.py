from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from app.get_user import *
from pydantic import BaseModel


router = APIRouter()

@router.get("/profile")
async def get_profile(request: Request):
    with db_session:
        current_user =  get_user(request.headers)

        if current_user == None:     # no existe el usuario en la bd o no hay header
             return {'error': 'Invalid X-Token header'}

        current_user_data = {
            "username": current_user.username,
            "email": current_user.email,
            "avatar": current_user.avatar #puede ser Vacio
        }

    return current_user_data




