from flask import Flask, render_template
from neo4j import GraphDatabase

app = Flask(__name__)

# Configuración de la conexión a Neo4j
uri = "neo4j+s://069aae57.databases.neo4j.io"
username = "neo4j"
password = "psDe8tSPGORUcnklsI2tlTZasxbwuJ-kZ_SzUToh8cA"
driver = GraphDatabase.driver(uri, auth=(username, password))


def get_db_connection():
    return driver.session()


@app.route('/')
def home():
    return render_template('index.html', message="Bienvenido a la página principal")


@app.route('/usuarios')
def usuarios():
    session = get_db_connection()
    try:
        result = session.run("MATCH (u:Usuario) RETURN u")
        # Acceder a las propiedades de los nodos directamente
        usuarios = [{key: value for key, value in record['u'].items()}
                    for record in result]
        print(usuarios)
    finally:
        session.close()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/peliculas')
def peliculas():
    session = get_db_connection()
    try:
        result = session.run("MATCH (p:Pelicula) RETURN p")
        peliculas = [{key: value for key, value in record['p'].items()}
                     for record in result]
    finally:
        session.close()
    return render_template('peliculas.html', peliculas=peliculas)


if __name__ == '__main__':
    app.run(debug=True)
