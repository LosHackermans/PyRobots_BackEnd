from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from userSchema import signUpModel 
from models import User
from pony.orm import *

router = APIRouter()

@router.post('/signup')
async def signup(user: signUpModel):
    with db_session:
        usernameQuery = select(e.username for e in User if (e.username == user.username))
        if len(usernameQuery) > 0:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail= "User with this username already exists")
        emailQuery = select(e.email for e in User if (e.email == user.email))
        if len(emailQuery) > 0:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail= "User with this email already exists")

        User(
        username = user.username,
        email = user.email,
        password = user.password,
        is_validated = False
    )

    return {"message": "User created successfully"}
