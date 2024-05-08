from flask import *
from neo4j import GraphDatabase
import csv

app = Flask(__name__)

# Configuración de la conexión a Neo4j
uri = "neo4j+ssc://069aae57.databases.neo4j.io"
username = "neo4j"
password = "psDe8tSPGORUcnklsI2tlTZasxbwuJ-kZ_SzUToh8cA"
driver = GraphDatabase.driver(uri, auth=(username, password))


def get_db_connection():
    return driver.session()


@app.route('/')
def home():
    return render_template('index.html')


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


@app.route('/NewUser', methods=['GET', 'POST'])
def NewUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('databases\\baseDatosUsuarios.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

        return redirect(url_for('home'))
    return render_template('NewUser.html')


if __name__ == '__main__':
    app.run(debug=True)