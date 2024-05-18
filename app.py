from flask import *
from neo4j import GraphDatabase
import csv

app = Flask(__name__)
app.secret_key = "trespelusas"

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

def leerBDUser(username, password):
    with open('databases/baseDatosUsuarios.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            #compara el nombre de usuario
            if row and row[0] == username and row[1]== password: 
                user_exists = True
                return  user_exists

@app.route('/User')
def User():
    if 'username' in session:
        username = session['username']
        return render_template('User.html', username=username)
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('LogUser'))

@app.route('/NewUser', methods=['GET', 'POST'])
def NewUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = False
        user_exists = leerBDUser(username, password)

        if user_exists:
            flash('El nombre de usuario ya está en uso, por favor elige otro.')
            return redirect(url_for('NewUser'))
        #Agregar el nuevo usuario a la base de datos
        with open('databases/baseDatosUsuarios.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
            flash('Usuario registrado exitosamente!')
        return redirect(url_for('home'))

    return render_template('NewUser.html')

@app.route('/LogUser', methods=['GET', 'POST'])
def LogUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = False
        user_exists = leerBDUser(username, password)

        if user_exists:
            flash('Ingreso exitoso')
            session['username'] = username  # Almacenar el nombre de usuario en la sesión
            return redirect(url_for('User'))

    return render_template('LogUser.html')

if __name__ == '__main__':
    app.run(debug=True)

