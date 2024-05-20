from flask import Flask, render_template, request, redirect, url_for, flash, session
from databases.Neo4jConfig import neo4j_conexion
from src.NewUser import leerBDUser, insertarUsuarioEnCSV, insertarUsuarioEnNeo4j
import csv

app = Flask(__name__)
app.secret_key = "trespelusas"


@app.route('/')
def home():
    return render_template('index.html')


def leerBDUser(username, password):
    with open('databases/baseDatosUsuarios.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # compara el nombre de usuario
            if row and row[0] == username and row[1] == password:
                user_exists = True
                return user_exists


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

        # Inserción en CSV y Neo4j
        insertarUsuarioEnCSV(username, password)
        insertarUsuarioEnNeo4j(username, password)

        flash('Usuario registrado exitosamente')
        return redirect(url_for('LogUser'))

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
            # Almacenar el nombre de usuario en la sesión
            session['username'] = username
            return redirect(url_for('User'))

    return render_template('LogUser.html')


if __name__ == '__main__':
    app.run(debug=True)
