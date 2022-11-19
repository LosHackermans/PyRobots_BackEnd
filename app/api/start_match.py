from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *


router = APIRouter()


@router.post("/start/{match_id}")
async def start_match(match_id):
    with db_session:
        The_Match = Match.get(lambda m: m.id == match_id)

        if The_Match == None:     # no existe el match
            return {'error': 'Invalid X-Token header'}

        match_is_ready_to_start = 2
        if (match_is_ready_to_start < 2 or match_is_ready_to_start > 4):
            match_is_ready_to_start = The_Match.robot_in_matches.count()

            return {"detail": "The match is not ready to start yet"}
        else:
            #Ejecutar partida, obtener el ganador(ganadores) y devolverlos al web soket!
            # {"Result": [{"User": "Pepito", "Robot": "Pepitron"}] }
            return {"detail": "The match has started"}



    # {
    #     "Result": [
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname},
    #              {"User": username, "Robot": robotname}
    #             ]
    # }
