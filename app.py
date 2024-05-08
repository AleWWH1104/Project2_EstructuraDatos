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

@app.route('/User')
def User():
    session = get_db_connection()
    return render_template('User.html')

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
