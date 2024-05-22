import sys
import os
from databases.Neo4jConfig import neo4j_conexion

# Añadir el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Consultar la base de datos para encontrar el usuario por su nombre de usuario
class Neo4jLoader:
    def __init__(self, connection):
        self.connection = connection

    def assign_movies_to_users(self, username, genres, viewflag):
        with self.connection.get_session() as session:
            if viewflag:
                movie_names = genres
            else:
                prefijo = "general"
                movie_names = [prefijo + genre.replace(' ', '') for genre in genres]
            
            print(movie_names)
            for movie_name in movie_names:
                session.write_transaction(self._create_relationship, username, movie_name)

    @staticmethod
    def _create_relationship(tx, username, movie_name):
        query = (
            "MATCH (u:User {name: $username}), (m:Movie {name: $movie_name}) "
            "MERGE (u)-[:LIKES]->(m)"
        )
        tx.run(query, username=username, movie_name=movie_name)

# Inicializar la conexión a Neo4j
neo4j_loader = Neo4jLoader(neo4j_conexion)

def assign_relations(username, genres, viewFlag=False):
    neo4j_loader.assign_movies_to_users(username, genres, viewFlag)
