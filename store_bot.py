import subprocess
from pony.orm import db_session


#parametros: userID, nombre, código, avatar (algun dia)
def store_bot_from_form(userID: int, name: str, raw_script_code: str) -> (bool, str):
    print("store_bot_from_form called")
    #dumpear la string a un archivo con el nombre de la clase del robot
    with open('temp_bot.py', 'w', encoding="utf-8") as temp_file:
        temp_file.write(raw_script_code)
    
    temp_file.close()
    
    #extracted_bot_name = extraer nombre del bot acá (en realidad asignarle un id)
    cmd = "mv temp_bot.py ./robots/{}.py}".format(extracted_bot_name)
    returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    print('returned value:', returned_value)

    #llamar BD para pasarle los datos del archivo creado, userID, etc...

    
    #devolver código de error
    return (True, "Robot almacenado con éxito!")
