import sys
import os, random

# Añadir el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from databases.Neo4jConfig import neo4j_conexion

def vecinoSimilar(username):
    query = """
    MATCH (u1:User {name: $username})-[:LIKES]->(m:Movie)<-[:LIKES]-(u2:User)
    WHERE u1 <> u2
    WITH u2, COLLECT(m.name) AS movies
    RETURN u2.name AS similar_user, movies
    """
    parameters = {'username': username}
    
    with neo4j_conexion.get_session() as session:
        results = session.run(query, parameters)
        similar_users = []
        for record in results:
            similar_user = record['similar_user']
            movies = record['movies']
            similar_users.append((similar_user, movies))
    
    return similar_users

def getMoviesVecino(username, otro_usuario):
    query = """
    MATCH (u1:User {name: $username})-[:LIKES]->(m:Movie)
    MATCH (u2:User {name: $otro_usuario})-[:LIKES]->(m2:Movie)
    WHERE NOT (u1)-[:LIKES]->(m2)
    RETURN COLLECT(m2.name) AS peliculas_otro_usuario
    """
    parameters = {'username': username, 'otro_usuario': otro_usuario}
    
    with neo4j_conexion.get_session() as session:
        result = session.run(query, parameters)
        return result.single()['peliculas_otro_usuario']

# Usamos conjuntos para evitar duplicados
usuarios_vistos = set()
peliculas_diferentes = set()

def getRecommendedMovies(username, movies_vecinos):
    for user, movies in movies_vecinos:
        usuarios_vistos.add(user)
        peliculas_diferentes.update(getMoviesVecino(username, user))

def aleatoryMovies(movies):
    cant = 10
    selectedMovies = random.sample(movies, cant)
    return selectedMovies

def movieDiccionaries(movies):
    movie_Dicc = []
    for movie in movies:
        query = """
        MATCH (m:Movie {name: $movie})-[:IN_GENRE]->(g:Genre)
        MATCH (m)-[:HAS_DURATION]->(d:Duration)
        RETURN m.name AS name, g.name AS genre, m.year AS year, d.time AS duration
        """
        parameters = {'movie': movie}

        with neo4j_conexion.get_session() as session:
            result = session.run(query, parameters)
            for record in result:
                movie_Dicc.append({
                    'name': record['name'],
                    'genre': record['genre'],
                    'year': record['year'],
                    'duration': record['duration']
                })
    return movie_Dicc

# Cerrar la conexión
neo4j_conexion.close()
