# necesario para correr los test (hecho en consola)
from app.api.models import *
from pony.orm import *
with db_session:
#   drop_all_tables(with_all_data=True)
    User(username = "as", email = "fama@gmail.com", password = "s", is_validated = True)
    User(username = "a", email = "f@gmail.com", password = "f", is_validated = True)
    User(username = "b", email = "fa@gmail.com", password = "c", is_validated = True)
    Robot(name = "ej", script = "asd",  user=User.get( email="f@gmail.com"))
    Robot(name = "ej2", script = "asd", user=User.get( email="f@gmail.com"))