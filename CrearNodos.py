from neo4j import GraphDatabase
import csv
# Configuración de la conexión a Neo4j
uri = "neo4j+ssc://069aae57.databases.neo4j.io"
username = "neo4j"
password = "psDe8tSPGORUcnklsI2tlTZasxbwuJ-kZ_SzUToh8cA"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Función para crear nodos de usuarios
def nodosUsers(tx, user, password):
    tx.run("CREATE (u:User {username: $user, password: $password})", user=user, password=password)

# Función para crear nodos de usuarios
def nodosPeliculas(tx, id_movie, movie, genre, year, duration):
    tx.run("CREATE (m:Pelicula {idMovie: $id, title: $title, year: $year, duration: $duration}) "
            "CREATE (g:Genero {name: $genre}) "
            "CREATE (d:Duracion {value: $duration}) "
            "CREATE (m)-[:BELONGS_TO_GENRE]->(g) "
            "CREATE (m)-[:HAS_DURATION]->(d)",id=id_movie, title=movie, genre=genre, year=year, duration=duration)

#CSV
UserCSV = "/Users/alejandraayala/Documents/Trabajos_UVG/Semestre 3/EstructuraDatos/Project2_EstructuraDatos/databases/baseDatosUsuarios.csv"
PeliculasCSV = ""

# Leer el CSV y crear nodos usuarios
with open(UserCSV, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        with driver.session() as session:
            session.write_transaction(nodosUsers, row['Usuario'], row['Contraseña'])

# Leer el CSV y crear nodos pelicula
with open(PeliculasCSV, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
