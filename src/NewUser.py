import csv
from databases.Neo4jConfig import neo4j_conexion


def insertarUsuarioEnCSV(username, password):
    with open('databases/baseDatosUsuarios.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])


def insertarUsuarioEnNeo4j(username, password):
    session = neo4j_conexion.get_session()
    query = "CREATE (u:User {username: $username, password: $password})"
    session.run(query, username=username, password=password)
    session.close()
