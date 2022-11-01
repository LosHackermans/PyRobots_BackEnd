from fastapi import FastAPI, Request, HTTPException, status
import jwt
from pydantic import BaseModel
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import *

router = APIRouter()


class Body(BaseModel):
    name: str
    avatar: str        
    script: str


@router.post("/upload_robot")
async def user_create_bot(body: Body, request: Request):
    with db_session:
        curent_user = get_user(request.headers)
        if curent_user == None:     # no existe el usuario en la bd o no hay header
            return {'error': 'Invalid X-Token header'}
        user_has_bot_already = select(r.name for r in User[curent_user.id].robots if (r.name == body.name))
        if len(user_has_bot_already) > 0: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="robot with this name already exists")
        robot = Robot(name=body.name, avatar = body.avatar, script=body.script,
                      user=curent_user)
        commit()
        return {'detail': "Robot created"}
