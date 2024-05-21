import csv
import sys
import os

# Añadir el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from databases.Neo4jConfig import neo4j_conexion

# Consultar la base de datos para encontrar el usuario por su nombre de usuario


def auth_user(username, password):
    with neo4j_conexion.get_session() as session:
        result = session.run(
            "MATCH (u:User {name: $username}) RETURN u.password AS password", username=username)
        record = result.single()

        # Verificar si se encontró el usuario y si la contraseña coincide
        if record and record['password'] == password:
            return True
        else:
            return False
        
def exist_user(username):
    with neo4j_conexion.get_session() as session:
        result = session.run(
            "MATCH (u:User {name: $username}) RETURN u", username=username)
        record = result.single()
        print(record)

        # Verificar si se encontró el usuario
        if record!=None:
            return True
        else:
            return False

def insertarUsuarioEnCSV(username, password):
    with open('databases/baseDatosUsuarios.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Username', 'Password'])
        writer.writerow({'Username': username, 'Password': password})

    
def insertarUsuarioEnNeo4j(username, password):
    session = neo4j_conexion.get_session()
    query = "CREATE (u:User {id: $username, name: $username, password: $password})"
    session.run(query, username=username, password=password)
    session.close()
