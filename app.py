from flask import *
from databases.Neo4jConfig import neo4j_conexion
from src.ManageUser import *
from src.ManageRelations import *

app = Flask(__name__)
app.secret_key = "trespelusas"

# Inicio de programa


@app.route('/')
def home():
    return render_template('index.html')

# Iniciar sesion usuario


@app.route('/LogUser', methods=['GET', 'POST'])
def LogUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = False
        user_exists = auth_user(username, password)

        if user_exists:
            flash('Ingreso exitoso')
            # Almacenar el nombre de usuario en la sesión
            session['username'] = username
            return redirect(url_for('User'))
    return render_template('LogUser.html')


@app.route('/NewUser', methods=['GET', 'POST'])
def NewUser():
    if request.method == 'POST':
        data = request.json  # Obtener los datos enviados desde el cliente

        username = data['username']
        password = data['password']
        selected_genres = data['selectedGenres']
        selected_duration = [data['selectedDuration'][:-1]]
        print(selected_genres)
        print(selected_duration)

        user_exists = False
        user_exists = auth_user(username, password)

        if user_exists:
            flash('El nombre de usuario ya está en uso, por favor elige otro.')
            return redirect(url_for('NewUser'))
        # Agregar el nuevo usuario a la base de datos
        else:
            insertarUsuarioEnCSV(username, password)
            insertarUsuarioEnNeo4j(username, password)
            assign_relations(username, selected_genres)
            assign_relations(username, selected_duration)

            flash('Usuario registrado exitosamente!')
            
        return jsonify({'message': 'Usuario registrado exitosamente!'})

    return render_template('NewUser.html')

@app.route('/User')
def User():
    if 'username' in session:
        username = session['username']
        return render_template('User.html', username=username)
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('LogUser'))


if __name__ == '__main__':
    app.run(debug=True)
