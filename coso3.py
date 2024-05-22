from neo4j import GraphDatabase
import random

uri = "neo4j+ssc://069aae57.databases.neo4j.io"
username = "neo4j"
password = "psDe8tSPGORUcnklsI2tlTZasxbwuJ-kZ_SzUToh8cA"

class Neo4jLoader:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def create_genre_movies(self, genres):
        with self.driver.session() as session:
            movie_id = 0  # Starting ID for new movies
            year = "5000"  # Setting the same year for simplicity
            for genre in genres:
                movie_name = f"general{genre.replace(' ', '')}"
                session.write_transaction(self._create_movie, str(movie_id), movie_name, genre, year)
                movie_id -= 1

    def assign_movies_to_users(self, user_ids):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Movie) WHERE m.id >= '1000' RETURN m.id AS movie_id")
            movie_names = ['generalDocumentary', 'generalComedy', 'generalHorror', 'generalAction', 'generalDrama', 'generalAdventure', 'generalRomanticComedy', 'generalMusical']


            for user_id in user_ids:
                selected_movies = random.sample(movie_names, 3)
                for movie_id in selected_movies:
                    session.write_transaction(self._create_relationship, user_id, movie_id)

    @staticmethod
    def _create_movie(tx, movie_id, movie_name, genre, year):
        query = (
            "MERGE (m:Movie {id: $movie_id, name: $movie_name, year: $year})"
            "MERGE (g:Genre {name: $genre})"
            "MERGE (m)-[:IN_GENRE]->(g)"
        )
        tx.run(query, movie_id=movie_id, movie_name=movie_name, genre=genre, year=year)

    @staticmethod
    def _create_relationship(tx, user_id, movie_id):
        query = (
            "MATCH (u:User {id: $user_id}), (m:Movie {name: $movie_id}) "
            "MERGE (u)-[:LIKES]->(m)"
        )
        print(user_id, movie_id)
        print(query)
        tx.run(query, user_id=user_id, movie_id=movie_id)


# Inicializar la conexión a Neo4j
neo4j_loader = Neo4jLoader(uri, username, password)

# Lista de géneros
genres = [
    "Documentary",
    "Comedy",
    "Horror",
    "Action",
    "Drama",
    "Adventure",
    "Romantic Comedy",
    "Musical"
]

# Crear nodos de películas basados en géneros
neo4j_loader.create_genre_movies(genres)

# Obtener la lista de usuarios ya presentes en la base de datos
with neo4j_loader.driver.session() as session:
    result = session.run("MATCH (u:User) RETURN u.id AS user_id")
    user_ids = [record["user_id"] for record in result]

# Asignar 3 películas aleatorias a cada usuario
neo4j_loader.assign_movies_to_users(user_ids)

# Cerrar la conexión a Neo4j
neo4j_loader.close()