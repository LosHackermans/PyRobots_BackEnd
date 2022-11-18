from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
import os
from app.api.upload_robot import Body
from robots.files.default.CircleBot import CircleBot
from robots.files.default.SquareBot import SquareBot
from app.api.upload_robot import update_default_robot
router = APIRouter()


class signUpModel(BaseModel):
    username: str
    email: str
    password: str
    avatar: str

    class Config:
        schema_extra = {
            'example': {
                "username": "Juan",
                "email": "juanperez@gmail.com",
                "password": "password"
            }
        }


@router.post('/create_user')
async def signup(user: signUpModel):
    with db_session:
        usernameQuery = select(
            e.username for e in User if (e.username == user.username))
        if len(usernameQuery) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this username already exists")
        emailQuery = select(e.email for e in User if (e.email == user.email))
        if len(emailQuery) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exists")
        if len(user.password) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The password must have a minimum of 8 characters")
        # if user.password != user.passwordRepeated:
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            # detail= "Passwords do not match")

        current_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            avatar=user.avatar,
            is_validated=False
        )

        # Upload default robots
        update_default_robot(CircleBot, current_user)
        update_default_robot(SquareBot, current_user)

    return {"message": "User created successfully"}
