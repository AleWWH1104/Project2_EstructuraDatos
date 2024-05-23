from flask import *
from src.ManageUser import *
from src.RecomendationSys import *
from src.ManageRelations import *

# Inicializa la aplicación Flask
app = Flask(__name__)
app.secret_key = "trespelusas"  # Clave secreta para sesiones y mensajes flash

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para iniciar sesión
@app.route('/LogUser', methods=['GET', 'POST'])
def LogUser():
    username = None
    if request.method == 'POST':  # Si se recibe un formulario por POST
        username = request.form['username']
        password = request.form['password']

        # Autentica al usuario
        user_exists = auth_user(username, password)

        if user_exists:  # Si la autenticación es exitosa
            flash('Ingreso exitoso')
            session['username'] = username  # Guarda el nombre de usuario en la sesión
            return redirect(url_for('User'))  # Redirige a la página del usuario
        else:
            flash('Nombre de usuario o contraseña incorrectos.')  # Mensaje de error
    
    return render_template('LogUser.html')  # Muestra el formulario de inicio de sesión

# Ruta para registrar un nuevo usuario
@app.route('/NewUser', methods=['GET', 'POST'])
def NewUser():
    if request.method == 'POST':  # Si se recibe un formulario por POST
        data = request.json
        username = data['username']
        password = data['password']
        selected_genres = data['selectedGenres']
        selected_duration = [data['selectedDuration'][:-1]]  # Recorta el último carácter de la duración
        
        # Verifica si el usuario ya existe
        user_exists = exist_user(username)
        if user_exists:
            flash('El nombre de usuario ya está en uso, por favor elige otro.')
            return jsonify({'message': 'El nombre de usuario ya está en uso.'}), 400
        else:
            # Inserta el usuario en la base de datos y asigna relaciones
            insertarUsuarioEnCSV(username, password)
            insertarUsuarioEnNeo4j(username, password)
            assign_relations(username, selected_genres)
            assign_relations(username, selected_duration)
            session['username'] = username  # Inicia sesión automáticamente
            flash('Usuario registrado exitosamente!')
            return jsonify({'message': 'Usuario registrado exitosamente!'}), 200

    return render_template('NewUser.html')  # Muestra el formulario de registro

# Ruta para la página del usuario
@app.route('/User', methods=['GET', 'POST'])
def User():
    if 'username' in session:  # Verifica si el usuario ha iniciado sesión
        username = session['username']
        if request.method == 'POST':  # Si se recibe un formulario por POST
            data = request.get_json()
            movie_name = [data.get('movie_name')]
            print(movie_name)
            assign_relations(username, movie_name, True)  # Asigna la película al usuario
            return jsonify({'message': f'Película {movie_name} asignada a {username}'})
        
        # Obtiene recomendaciones de películas basadas en vecinos similares y otros criterios
        movies_vecinos = vecinoSimilar(username)
        getRecommendedMovies(username, movies_vecinos)
        randomMovies = aleatoryMovies(peliculas_diferentes)
        diccionario1 = movieDiccionaries(randomMovies)
        generes = genrMoreView(username)
        d1, d2, d3 = recomend_geners_movie(generes)
        
        return render_template('User.html', username=username, diccionario1=diccionario1, diccionario2=d1, diccionario3=d2, diccionario4=d3, Genero1=generes[0], Genero2=generes[1], Genero3=generes[2])
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('LogUser'))  # Redirige al formulario de inicio de sesión si no ha iniciado sesión

# Inicia la aplicación Flask en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)