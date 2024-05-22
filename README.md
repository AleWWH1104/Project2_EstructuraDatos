# Project2_EstructuraDatos
# Sistema de Recomendaciones de Películas

## Descripción del Proyecto

Este proyecto consiste en un sistema de recomendaciones de películas que utiliza el algoritmo del vecino similar. El objetivo es proporcionar a los usuarios recomendaciones personalizadas basadas en sus hábitos de visualización y géneros favoritos. 

## Funcionalidad del Sistema

El sistema opera de la siguiente manera:
1. **Registro de Usuario**: 
   - Los usuarios deben registrarse proporcionando un nombre de usuario, una contraseña, seleccionando obligatoriamente tres géneros de películas favoritos y la duración preferida de las películas.
   - Si el nombre de usuario ya existe, se mostrará una alerta en la consola y no dejar avanzar en el botón continuar.

2. **Inicio de Sesión**:
   - Los usuarios registrados pueden iniciar sesión con sus credenciales.
   - Al ingresar, el sistema mostrará recomendaciones de películas basadas en las películas vistas y los géneros favoritos del usuario.

3. **Ver Película**:
   - Al seleccionar el botón "ver película", el sistema captura el nombre de la película y la asocia con el usuario en la base de datos.
   - Esto permite al sistema acumular el historial de visualización del usuario y actualizar las recomendaciones de acuerdo con los géneros más vistos.

4. **Recomendaciones**:
   - El sistema analiza las películas vistas por el usuario y extrae los tres géneros más vistos.
   - Basado en estos géneros y las películas vistas por otros usuarios con intereses similares, el sistema recomienda nuevas películas.

## Instrucciones de Uso

1. **Ejecución del Programa**:
   - Ejecutar el archivo `app.py`.
   - Copiar el enlace de la dirección IP, puerto y ruta para acceder al host del servidor.

## Recursos Utilizados

- **Frontend**:
  - HTML, CSS y JavaScript para la interfaz de usuario y mecanismos de interacción.

- **Backend**:
  - Flask para correr el programa y manejar las rutas del servidor.

- **Base de Datos**:
  - Neo4j para manejar la base de datos basada en grafos, lo que facilita las relaciones entre usuarios y películas.
  - Archivos CSV para llenar la base de datos con datos iniciales.

## Integrantes
Iris Ayala, Jonathan Diaz, Anggie Quezada
---

¡Gracias por usar nuestro Sistema de Recomendaciones de Películas! Esperamos que disfrutes de las recomendaciones personalizadas y descubras nuevas películas favoritas.