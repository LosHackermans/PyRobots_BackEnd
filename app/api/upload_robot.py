from fastapi import FastAPI, Request, HTTPException, status
import jwt
from pydantic import BaseModel
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter

router = APIRouter()
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

class Body(BaseModel):
    name: str
    avatar: str        
    script: str


def get_current_user(data):
    current_user_info = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    current_user = User.get(email=current_user_info["email"])
    return current_user

@router.post("/upload_robot")
async def user_create_bot(body: Body, request: Request):
    with db_session:
        token = request.headers.get("authorization")
        print(request.headers)
        if token[0:7] != "Bearer ":
            return {'error': 'Invalid header'}
        else:
            token = token[7:]
        curent_user = get_current_user(token)
        if curent_user == None:     # no existe el usuario en la bd
            return {'error': 'Invalid X-Token header'}
        user_has_bot_already = select(r.name for r in User[curent_user.id].robots if (r.name == body.name))
        if len(user_has_bot_already) > 0: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="robot with this name already exists")
        robot = Robot(name=body.name, avatar = body.avatar, script=body.script,
                      user=curent_user)
        commit()
        return {'detail': "Robot created"}
