import csv
import random

# Nombre del archivo CSV
filename = 'databases/basePelis.csv'

# Leer el archivo CSV y almacenar los datos
movies = []
with open(filename, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        movies.append(row)

# Función para filtrar y seleccionar películas por género
def sort_by_genre(movies, genre):
    filtered_movies = [movie for movie in movies if movie['Genre'].strip().lower() == genre.lower()]
    selected_movies = random.sample(filtered_movies, min(len(filtered_movies), 10))
    return selected_movies

# Solicitar el género al usuario
genre = input("Ingrese el género de las películas que desea ver: ")

# Obtener y mostrar las películas seleccionadas
selected_movies = sort_by_genre(movies, genre)
for movie in selected_movies:
    print(f"IdMovie: {movie['IdMovie']}, Movie: {movie['Movie']}, Genre: {movie['Genre']}, Year: {movie['Year']}, Duracion: {movie['Duracion']}")
