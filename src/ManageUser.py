from databases.Neo4jConfig import neo4j_conexion 
from flask import *

# Consultar la base de datos para encontrar el usuario por su nombre de usuario
def auth_user(username, password):
    with neo4j_conexion.get_session() as session:
        result = session.run("MATCH (u:User {name: $username}) RETURN u.password AS password", username=username)
        record = result.single()

        # Verificar si se encontró el usuario y si la contraseña coincide
        if record and record['password'] == password:
            return True
        else:
            return False
        
# def register_User():
#     with neo4j_conexion.get_session() as session:

