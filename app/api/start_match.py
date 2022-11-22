from fastapi import APIRouter, FastAPI, Request, HTTPException, status, WebSocket
from app.api.models import *
from pony.orm import db_session
import json
from pydantic import BaseModel
from app.get_user import *
import websockets

router = APIRouter()


async def start_match_websocket(match_id):
    async with websockets.connect(f"ws://localhost:8000/lobby/{match_id}") as websocket:
        await websocket.send("start")
        await websocket.close()


@router.post("/start/{match_id}")
async def start_match(match_id):
    with db_session:
        The_Match = Match.get(lambda m: m.id == match_id)

        if The_Match == None:     # no existe el match
            return {'error': 'The match does not exist'}

        quantity_of_players = The_Match.robot_in_matches.count()

        if (quantity_of_players < The_Match.min_players):
            return {"detail": "The match is not ready to start yet"}

        else:
            await start_match_websocket(match_id)
            The_Match.is_joinable = False
            The_Match.is_finished = True
            return {"detail": "The match has started"}
