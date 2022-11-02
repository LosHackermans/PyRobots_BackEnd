from pony.orm import db_session
import jwt
from app.api.models import User

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

def get_user(header):
     with db_session:
            token = header.get("authorization")
            if token is None or token[0:7] != "Bearer " :
                return None
            else:
                token = token[7:]
            current_user_info = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            current_user = User.get(email=current_user_info["email"])
            return current_user