from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *


router = APIRouter()


@router.post("/start/{match_id}")
async def start_match(match_id):

    The_Match = Match.get(lambda m: m.id == match_id)
    match_is_ready_to_start = 1
    if (match_is_ready_to_start < 2):
        match_is_ready_to_start = 0
        for user_in_match in The_Match.robot_in_matches:
            match_is_ready_to_start += 1

        return {"detail": "The match is not ready to start yet"}
    else:
        #Ejecutar partida, obtener el ganador(ganadores) y devolverlos
        return {"Result": [{"User": "Pepito", "Robot": "Pepitron"}] }



    # {
    #     "Result": [
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname}
    #             ]
    # }
