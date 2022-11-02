## Pautas del Código:

#### Master (Rama Principal)

- Sólo se utiliza para releases (demos).
- Para una release se hace un merge de develop hacia master, y se crea un tag (v1, v2, v3)
```bash
$ git tag <tag_name> <commit_hash>
```

#### Develop
- Branch base para el desarrollo. Para comenzar a desarrollar una feature o bugfix, se branchea desde acá
- Sólo se mergea hacia esta rama tareas que estén completadas (revisadas y testeadas)
- Esta rama no puede estar en estado no funcional

#### Feature branches
- Se crean para cada ticket
- Mantener el formato de JIRA:
		feature_PYR-'NUM'_*, bugfix_PYR-'NUM'_*
		Ejemplo: feature_PYR-16_Crear_app_React
	Utilizar el JIRA_CODE como prefijo para los commits


### Instrucciones para correr el back
- run: uvicorn app.main:app
- test: 
(eliminar db si existe)
python3 montardbtest.py
python3 -m pytest
coverage run -m --source=test pytest && coverage report -m
------------
