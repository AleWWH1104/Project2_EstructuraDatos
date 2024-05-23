import csv
import sys
import os

# Añadir el directorio raíz al sys.path para permitir importaciones de módulos desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from databases.Neo4jConfig import neo4j_conexion

# Función para autenticar a un usuario
def auth_user(username, password):
    with neo4j_conexion.get_session() as session:  # Inicia una sesión con la base de datos Neo4j
        result = session.run(
            "MATCH (u:User {name: $username}) RETURN u.password AS password", username=username)
        record = result.single()  # Obtiene un solo registro del resultado de la consulta

        # Verificar si se encontró el usuario y si la contraseña coincide
        if record and record['password'] == password:
            return True
        else:
            return False

# Función para verificar si un usuario ya existe
def exist_user(username):
    with neo4j_conexion.get_session() as session:  # Inicia una sesión con la base de datos Neo4j
        result = session.run(
            "MATCH (u:User {name: $username}) RETURN u", username=username)
        record = result.single()  # Obtiene un solo registro del resultado de la consulta
        print(record)  # Imprime el registro (para depuración)

        # Verificar si se encontró el usuario
        if record is not None:
            return True
        else:
            return False

# Función para insertar un nuevo usuario en un archivo CSV
def insertarUsuarioEnCSV(username, password):
    with open('databases/baseDatosUsuarios.csv', 'a', newline='') as file:  # Abre el archivo CSV en modo de añadido
        writer = csv.DictWriter(file, fieldnames=['Username', 'Password'])  # Crea un escritor de diccionario
        writer.writerow({'Username': username, 'Password': password})  # Escribe una fila con el nombre de usuario y la contraseña

# Función para insertar un nuevo usuario en la base de datos Neo4j
def insertarUsuarioEnNeo4j(username, password):
    session = neo4j_conexion.get_session()  # Inicia una sesión con la base de datos Neo4j
    query = "CREATE (u:User {id: $username, name: $username, password: $password})"  # Consulta para crear un nuevo nodo de usuario
    session.run(query, username=username, password=password)  # Ejecuta la consulta con los parámetros proporcionados
    session.close()  # Cierra la sesión