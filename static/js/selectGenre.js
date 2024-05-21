const maxSelections = 3;
let selectedGenres = [];

function selectGenre(button) {
	const genre = button.textContent;

	if (selectedGenres.includes(genre)) {
		selectedGenres = selectedGenres.filter(g => g !== genre);
		button.classList.remove('selected');
	} else {
		if (selectedGenres.length < maxSelections) {
			selectedGenres.push(genre);
			button.classList.add('selected');
		} else {
			alert("Solo puedes seleccionar hasta 3 géneros.");
		}
	}
	console.log(selectedGenres);
}

function updateSelectedGenres() {
	document.getElementById('selectedGenres').value = selectedGenres.join(',');
}

function getGenre() {
	return selectedGenres;
}


function selectDuration(button) {
	// Remover la clase "selected" de todos los botones
	document.querySelectorAll('.container-final button').forEach(btn => btn.classList.remove('selected'));

	// Agregar la clase "selected" al botón seleccionado
	button.classList.add('selected');
}

function continueProcess() {
	var username = document.getElementById('username').value;
	var password = document.getElementById('password').value;
	var selectedGenres = getGenre();  // Esta función obtiene los géneros seleccionados del JavaScript

	// Obtener la duración seleccionada
	var selectedDuration = document.querySelector('.container-final button.selected').textContent;

	// Crear un objeto con los datos a enviar
	var data = {
		username: username,
		password: password,
		selectedGenres: selectedGenres,
		selectedDuration: selectedDuration
	};

	// Enviar los datos al servidor mediante una solicitud AJAX
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/NewUser", true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			// Redireccionar a donde desees después de enviar los datos exitosamente
			window.location.href = "/LogUser";  // Cambia "/redirect_page" por la URL deseada
		} else {
			// Manejar cualquier error que ocurra durante la solicitud
			console.error('Error:', xhr.responseText);
		}
	};
	xhr.send(JSON.stringify(data));
}

