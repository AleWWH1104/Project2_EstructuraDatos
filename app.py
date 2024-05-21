from flask import *
import csv
from src.ManageUser import *
from src.RecomendationSys import *

app = Flask(__name__)
app.secret_key = "trespelusas"

#Inicio de programa
@app.route('/')
def home():
    return render_template('index.html')

#Iniciar sesion usuario
@app.route('/LogUser', methods=['GET', 'POST'])
def LogUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = False
        user_exists = auth_user(username, password)

        if user_exists:
            flash('Ingreso exitoso')
            session['username'] = username  # Almacenar el nombre de usuario en la sesión
            return redirect(url_for('User'))
    return render_template('LogUser.html')

@app.route('/NewUser', methods=['GET', 'POST'])
def NewUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = False
        user_exists = auth_user(username, password)

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

@app.route('/User')
def User():
    if 'username' in session:
        username = session['username']
        movies_vecinos = vecinoSimilar(username)
        getRecommendedMovies(username,movies_vecinos)
        randomMovies = aleatoryMovies(peliculas_diferentes)
        diccionario1 = movieDiccionaries(randomMovies)
        return render_template('User.html', username=username, diccionario=diccionario1)
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('LogUser'))

if __name__ == '__main__':
    app.run(debug=True)

