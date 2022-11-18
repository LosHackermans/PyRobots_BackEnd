from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *


router = APIRouter()


@router.post("/start/{match_id}")
async def start_match():






    # {
    #     "Result": [
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname}
    #             ]
    # }
