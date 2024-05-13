function generarCarrusel(idContenedor, cantidadCartas) {
    const carruselContainer = document.getElementById(idContenedor);

    // Bucle para generar las cartas
    for (let i = 0; i < cantidadCartas; i++) {
        // Crea un div para cada carta
        const cartaDiv = document.createElement('div');
        cartaDiv.classList.add('swiper-slide');

        // Agrega el contenido de la carta
        cartaDiv.innerHTML = `
            <h3>Título ${i + 1}</h3>
            <h3>Género</h3>
            <h3>Duración</h3>
            <h3>Año</h3>
        `;

        // Agrega la carta al contenedor
        carruselContainer.appendChild(cartaDiv);
    }
}

// Llama a la función para generar los carruseles
generarCarrusel('carrusel-container-1', 10); // Primer carrusel
generarCarrusel('carrusel-container-2', 10);
generarCarrusel('carrusel-container-3', 10);
generarCarrusel('carrusel-container-4', 10);
generarCarrusel('carrusel-container-5', 10);
var swiper = new Swiper('.swiper-container', {
	navigation: {
	  nextEl: '.swiper-button-next',
	  prevEl: '.swiper-button-prev'
	},
	slidesPerView: 1,
	spaceBetween: 10,
	// init: false,
	pagination: {
	  el: '.swiper-pagination',
	  clickable: true,
	},

  
	breakpoints: {
	  620: {
		slidesPerView: 1,
		spaceBetween: 20,
	  },
	  680: {
		slidesPerView: 2,
		spaceBetween: 40,
	  },
	  920: {
		slidesPerView: 4,
		spaceBetween: 50,
	  },
	  1240: {
		slidesPerView: 5,
		spaceBetween: 50,
	  },
	} 
});