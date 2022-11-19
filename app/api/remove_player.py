from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *


router = APIRouter()


@router.post("/abandon/{match_id}")
async def remove_user_from_match(request: Request, match_id):
    
    with db_session:
        current_user =  get_user(request.headers)
        if current_user == None:     # no existe el usuario en la bd o no hay header
            return {'error': 'Invalid X-Token header'}

        match = Match.get(id=match_id)
        for robot_o in match.robot_in_matches:
            for other_robot in current_user.robots:
                if (robot_o.robot.id == other_robot.id):
                    robot_o.delete()

    return {"detail": "User remove successful from the match"}
