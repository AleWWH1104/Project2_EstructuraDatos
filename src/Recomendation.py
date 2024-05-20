import sys
import os
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

def obtenerPeliculasDiferentes(username, otro_usuario):
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

user_name = "batman4"  # Reemplaza esto con el nombre del usuario que deseas buscar
similar_users = vecinoSimilar(user_name)

# Usamos conjuntos para evitar duplicados
usuarios_vistos = set()
peliculas_diferentes = set()

for user, movies in similar_users:
    usuarios_vistos.add(user)
    peliculas_diferentes.update(obtenerPeliculasDiferentes(user_name, user))

print("Usuarios similares:")
for user in usuarios_vistos:
    print(f"- {user}")

print("\nPelículas diferentes de los usuarios similares:")
contar = 0
for movie in peliculas_diferentes:
    contar +=1
    print(f"{contar}- {movie}")

neo4j_conexion.close()
