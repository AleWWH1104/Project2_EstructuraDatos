from neo4j import GraphDatabase
import csv
import random

uri = "neo4j+ssc://069aae57.databases.neo4j.io"
username = "neo4j"
password = "psDe8tSPGORUcnklsI2tlTZasxbwuJ-kZ_SzUToh8cA"


class Neo4jLoader:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def insert_user(self, user_id, user_name, user_password):
        with self.driver.session() as session:
            session.write_transaction(
                self._create_user, user_id, user_name, user_password)

    def relate_user_to_movies(self, user_id, movie_ids):
        with self.driver.session() as session:
            for movie_id in movie_ids:
                session.write_transaction(
                    self._create_relationship, user_id, movie_id)

    @staticmethod
    def _create_user(tx, user_id, user_name, user_password):
        query = (
            "MERGE (u:User {id: $user_id, name: $user_name, password: $user_password})"
        )
        tx.run(query, user_id=user_id, user_name=user_name,
               user_password=user_password)

    @staticmethod
    def _create_relationship(tx, user_id, movie_id):
        query = (
            "MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id}) "
            "MERGE (u)-[:LIKES]->(m)"
        )
        tx.run(query, user_id=user_id, movie_id=movie_id)


# Nombre del archivo CSV y ruta si es necesario
csv_file = 'databases\\baseDatosPelis.csv'

# Inicializar la conexión a Neo4j
neo4j_loader = Neo4jLoader(uri, username, password)

# Leer las películas del archivo CSV
movie_ids = []
with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        movie_id = row['\ufeffIdMovie']
        movie_ids.append(movie_id)

# Lista de usuarios y contraseñas
users = [
    ("batman4", "password123"),
    ("panito4", "qwerty456"),
    ("heroic5", "abc123"),
    ("galactic7", "password789"),
    ("swift9", "zxcvbnm"),
    ("stellar3", "qazwsxedc"),
    ("cosmic8", "passw0rd"),
    ("ninja6", "letmein"),
    ("phantom1", "12345678"),
    ("blaze2", "baseball"),
    ("raven12", "football"),
    ("falcon19", "monkey"),
    ("nebula11", "iloveyou"),
    ("shadow20", "admin"),
    ("comet13", "welcome"),
    ("mystic10", "trustno1"),
    ("vortex14", "dragon"),
    ("nova15", "freedom"),
    ("cyber17", "mustang"),
    ("orbit18", "password1"),
    ("eclipse16", "superman"),
    ("spectra21", "batman"),
    ("zenith22", "master"),
    ("lumina23", "sunshine"),
    ("quantum24", "shadow"),
    ("alpha25", "princess"),
    ("omega26", "asdfgh"),
    ("phoenix27", "qwertyuiop"),
    ("titan28", "whatever"),
    ("voyager29", "starwars")
]

# Generar usuarios y relaciones aleatorias
for user_id, user_password in users:
    neo4j_loader.insert_user(user_id, user_id, user_password)

    # Relacionar al usuario con una cantidad aleatoria de películas entre 3 y 20
    num_movies = random.randint(3, 20)
    user_movie_ids = random.sample(movie_ids, num_movies)
    neo4j_loader.relate_user_to_movies(user_id, user_movie_ids)

# Cerrar la conexión a Neo4j
neo4j_loader.close()