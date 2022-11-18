from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *


router = APIRouter()


@router.post("/abandon/{match_id}")
async def remove_user_from_match(match_id, request):
    current_user =  get_user(request.headers)

    for robot_o in match_id.robot_in_matches:
        for other_robot in current_user.robots:
            if (robot_o.robot.id == other_robot.id):
                match_id.remove(robot_o)

    return {"detail": "User remove successful from the match"}
