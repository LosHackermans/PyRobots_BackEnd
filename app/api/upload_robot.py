from fastapi import FastAPI, Request, HTTPException, status
import jwt
from pydantic import BaseModel
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import *
import os

router = APIRouter()


class Body(BaseModel):
    name: str
    avatar: str
    script: str
    fileName: str


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

        try:
            path = f'robots/files/{curent_user.username}'
            if not os.path.exists(path):
                os.makedirs(path)
            path_to_file = f'{path}/{body.fileName}'
            with open(path_to_file, 'a', encoding="utf-8") as temp_file:
                temp_file.write(body.script)
            temp_file.close()
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="robot couldn't be saved")

        robot = Robot(name=body.name, avatar = body.avatar, script=path_to_file,
                      user=curent_user)

        commit()
        return {'detail': "Robot created"}

def update_default_robot(robot: Body, current_user: User):
    with db_session:
        try:
            path = f'robots/files/{current_user.username}'
            if not os.path.exists(path):
                os.makedirs(path)
            path_to_file = f'{path}/{robot.fileName}'
            with open(path_to_file, 'a', encoding="utf-8") as temp_file:
                temp_file.write(robot.script)
            temp_file.close()
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="robot couldn't be saved")

        Robot(name=robot.name, avatar=robot.avatar,
              script=path_to_file, user=current_user)
        commit()
        return {'detail': "Robot created"}