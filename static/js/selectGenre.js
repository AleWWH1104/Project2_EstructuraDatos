const maxSelections = 3;
let selectedGenres = [];
let selectedDuration = "";

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

function selectDuration(button) {
	document.querySelectorAll('.container-final button').forEach(btn => btn.classList.remove('selected'));
	button.classList.add('selected');
	selectedDuration = button.textContent;
	console.log(selectedDuration);
}

function continueProcess() {
	// Obtener el botón y deshabilitarlo
    var submitButton = document.getElementById('submit-button');
    submitButton.disabled = true;

	var username = document.getElementById('username').value;
	var password = document.getElementById('password').value;

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
			// Redireccionar después de enviar los datos exitosamente
			window.location.href = "/User";  
		} else if (xhr.readyState === 4) {
			// Manejar cualquier error que ocurra durante la solicitud
			console.error('Error:', xhr.responseText);
		}
	};
	xhr.send(JSON.stringify(data));
}

