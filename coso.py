from neo4j import GraphDatabase
import csv

uri = "neo4j+ssc://069aae57.databases.neo4j.io"
username = "neo4j"
password = "psDe8tSPGORUcnklsI2tlTZasxbwuJ-kZ_SzUToh8cA"


class Neo4jLoader:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def insert_movie(self, movie_id, movie_name, genre, year, duration):
        with self.driver.session() as session:
            session.write_transaction(
                self._create_movie, movie_id, movie_name, year)
            session.write_transaction(self._create_genre, movie_id, genre)
            session.write_transaction(
                self._create_duration, movie_id, duration)

    @staticmethod
    def _create_movie(tx, movie_id, movie_name, year):
        query = (
            "MERGE (m:Movie {id: $movie_id, name: $movie_name, year: $year})"
        )
        tx.run(query, movie_id=movie_id, movie_name=movie_name, year=year)

    @staticmethod
    def _create_genre(tx, movie_id, genre):
        query = (
            "MERGE (g:Genre {name: $genre})"
            "MERGE (m:Movie {id: $movie_id})"
            "MERGE (m)-[:IN_GENRE]->(g)"
        )
        tx.run(query, movie_id=movie_id, genre=genre)

    @staticmethod
    def _create_duration(tx, movie_id, duration):
        query = (
            "MERGE (d:Duration {time: $duration})"
            "MERGE (m:Movie {id: $movie_id})"
            "MERGE (m)-[:HAS_DURATION]->(d)"
        )
        tx.run(query, movie_id=movie_id, duration=duration)


# Nombre del archivo CSV y ruta si es necesario
csv_file = 'databases\\baseDatosPelis.csv'

# Inicializar la conexión a Neo4j
neo4j_loader = Neo4jLoader(uri, username, password)

# Procesar el archivo CSV
with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        print(row)
        movie_id = row['\ufeffIdMovie']
        movie_name = row['Movie']
        genre = row['Genre']
        year = row['Year']
        duration = row['Duracion']

        # Insertar datos en Neo4j
        neo4j_loader.insert_movie(movie_id, movie_name, genre, year, duration)

# Cerrar la conexión a Neo4j
neo4j_loader.close()