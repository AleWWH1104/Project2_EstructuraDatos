import sys
import os
import random

# Añadir el directorio raíz al sys.path para permitir importaciones de módulos desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from databases.Neo4jConfig import neo4j_conexion

# Función para encontrar usuarios similares basados en las películas que les gustan
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

# Función para obtener películas que le gustan a otro usuario pero no al usuario dado
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

# Función para obtener recomendaciones de películas basadas en los vecinos similares
def getRecommendedMovies(username, movies_vecinos):
    for user, movies in movies_vecinos:
        usuarios_vistos.add(user)
        peliculas_diferentes.update(getMoviesVecino(username, user))

# Función para seleccionar películas aleatorias
def aleatoryMovies(movies):
    cant = 10
    selectedMovies = random.sample(movies, cant)
    return selectedMovies

# Función para obtener los géneros más vistos por un usuario
def genrMoreView(username):
    query = """
    MATCH (u:User {name: $username})-[:LIKES]->(m:Movie)-[:IN_GENRE]->(g:Genre)
    RETURN g.name AS genre, COUNT(m) AS count
    ORDER BY count DESC
    LIMIT 3
    """
    parameters = {'username': username}

    with neo4j_conexion.get_session() as session:
        result = session.run(query, parameters)
        top_genres = []
        for record in result:
            top_genres.append(record['genre'])
    
    return top_genres

# Función para recomendar películas basadas en los géneros más vistos
def recomend_geners_movie(generes):
    moviesList = []
    for genere in generes:
        movies = aleatoryMovies(obtener_nombres_peliculas_por_genero(genere))
        dics = movieDiccionaries(movies)
        moviesList.append(dics)

    return moviesList[0], moviesList[1], moviesList[2]

# Función para obtener nombres de películas por género
def obtener_nombres_peliculas_por_genero(genero):
    query = """
    MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name: $genero})
    RETURN m.name AS nombre_pelicula
    """
    parametros = {'genero': genero}
    
    with neo4j_conexion.get_session() as sesion:
        resultados = sesion.run(query, parametros)
        nombres_peliculas = [registro['nombre_pelicula'] for registro in resultados]
    
    return nombres_peliculas

# Función para crear diccionarios de películas con sus detalles
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

# Cerrar la conexión a Neo4j
neo4j_conexion.close()