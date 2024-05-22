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

    def create_genre_movies(self, durations):
        with self.driver.session() as session:
            for duration in durations:
                movie_name = f"general{duration}"
                session.write_transaction(self._create_movie, movie_name, duration)

    def assign_movies_to_users(self, user_ids):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Movie) WHERE m.name STARTS WITH 'general' RETURN m.name AS movie_name")
            movie_names = ["generalCorta", "generalLarga"]

            for user_id in user_ids:
                selected_movie = random.choice(movie_names)
                session.write_transaction(self._create_relationship, user_id, selected_movie)

    @staticmethod
    def _create_movie(tx, movie_name, duration):
        query = (
            "MERGE (m:Movie {name: $movie_name})"
            "WITH m "
            "MATCH (d:Duration) WHERE "
            "(m.name STARTS WITH 'generalLarga' AND toInteger(d.time) >= 90) OR "
            "(m.name STARTS WITH 'generalCorta' AND toInteger(d.time) < 90) "
            "MERGE (m)-[:HAS_DURATION]->(d)"
        )
        tx.run(query, movie_name=movie_name, duration=duration)

    @staticmethod
    def _create_relationship(tx, user_id, movie_name):
        query = (
            "MATCH (u:User {id: $user_id}), (m:Movie {name: $movie_name}) "
            "MERGE (u)-[:LIKES]->(m)"
        )
        print(user_id, movie_name)
        tx.run(query, user_id=user_id, movie_name=movie_name)


# Inicializar la conexión a Neo4j
neo4j_loader = Neo4jLoader(uri, username, password)

# Lista de duraciones
durations = ["Larga", "Corta"]

# Crear nodos de películas basados en duraciones
neo4j_loader.create_genre_movies(durations)

# Obtener la lista de usuarios ya presentes en la base de datos
with neo4j_loader.driver.session() as session:
    result = session.run("MATCH (u:User) RETURN u.id AS user_id")
    user_ids = [record["user_id"] for record in result]
print(user_ids)
# Asignar una película aleatoria a cada usuario
neo4j_loader.assign_movies_to_users(user_ids)

# Cerrar la conexión a Neo4j
neo4j_loader.close()