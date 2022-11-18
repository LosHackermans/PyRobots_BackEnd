from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *


router = APIRouter()


@router.post("/start/{match_id}")
async def start_match():

    match_is_ready_to_start = False
    if (!match_is_ready_to_start):
        return {"detail": "The match is not ready yet"}
    else:
        #Ejecutar partida, obtener el ganador(ganadores) y devolverlos




    # {
    #     "Result": [
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname}
    #             ]
    # }
