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

function getGenre(){
	return selectedGenres;
}
