# necesario para correr los test (hecho en consola)
from app.api.models import *
from pony.orm import *
with db_session:
#   drop_all_tables(with_all_data=True)
    User(username = "pedro", email = "famaf01@gmail.com", password = "nuevofamaf", is_validated = True)