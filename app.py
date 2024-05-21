from flask import *
from src.ManageUser import *
from src.RecomendationSys import *
from src.ManageRelations import *

app = Flask(__name__)
app.secret_key = "trespelusas"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/LogUser', methods=['GET', 'POST'])
def LogUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = auth_user(username, password)

        if user_exists:
            flash('Ingreso exitoso')
            session['username'] = username
            return redirect(url_for('User'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
    
    return render_template('LogUser.html')

@app.route('/NewUser', methods=['GET', 'POST'])
def NewUser():
    if request.method == 'POST':
        data = request.json
        username = data['username']
        password = data['password']
        selected_genres = data['selectedGenres']
        selected_duration = data['selectedDuration']

        user_exists = auth_user(username, password)

        if user_exists:
            flash('El nombre de usuario ya está en uso, por favor elige otro.')
            return jsonify({'message': 'El nombre de usuario ya está en uso.'}), 400
        else:
            insertarUsuarioEnCSV(username, password)
            insertarUsuarioEnNeo4j(username, password)
            assign_relations(username, selected_genres)
            assign_relations(username, selected_duration)
            session['username'] = username
            flash('Usuario registrado exitosamente!')
            return jsonify({'message': 'Usuario registrado exitosamente!'}), 200

    return render_template('NewUser.html')

@app.route('/User', methods=['GET', 'POST'])
def User():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            movie_name = ""
            assign_relations(username, movie_name)

        movies_vecinos = vecinoSimilar(username)
        getRecommendedMovies(username,movies_vecinos)
        randomMovies = aleatoryMovies(peliculas_diferentes)
        diccionario1 = movieDiccionaries(randomMovies)
        generes = genrMoreView(username)
        d1, d2, d3 =recomend_geners_movie(generes)
        return render_template('User.html', username=username, diccionario1=diccionario1, diccionario2=d1, diccionario3=d2, diccionario4=d3, Genero1=generes[0], Genero2=generes[1], Genero3=generes[2])
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('LogUser'))

if __name__ == '__main__':
    app.run(debug=True)
