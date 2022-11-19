from pydantic import BaseModel
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter

router = APIRouter()

class verficationModel(BaseModel):
    email: str
    token: str

@router.post('/validate_user')
async def validate_user(user: verficationModel):
    with db_session:
        currentuser = User.get(email=user.email)
        if currentuser.verify_token == None or currentuser.verify_token != user.token:
            return {"error": "incorrect token"}
        else:
            currentuser.is_validated = True
            return {"message": "valid token"}