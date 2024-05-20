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

var swiper1 = new Swiper('.mySwiper1', {
	navigation: {
	  nextEl: '#bn1',
	  prevEl: '#bp1'
	},
	slidesPerView: 1,
	spaceBetween: 10,
	// init: false,
	pagination: {
	  el: '.swiper-pagination-1',
	  clickable: true,
	},
	breakpoints: {
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

var swiper2 = new Swiper('.mySwiper2', {
	navigation: {
	  nextEl: '#bn2',
	  prevEl: '#bp2'
	},
	slidesPerView: 1,
	spaceBetween: 10,
	// init: false,
	pagination: {
	  el: '.swiper-pagination-2',
	  clickable: true,
	},
	breakpoints: {
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

var swiper3 = new Swiper('.mySwiper3', {
	navigation: {
	  nextEl: '#bn3',
	  prevEl: '#bp3'
	},
	slidesPerView: 1,
	spaceBetween: 10,
	// init: false,
	pagination: {
	  el: '.swiper-pagination-3',
	  clickable: true,
	},
	breakpoints: {
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

var swiper4 = new Swiper('.mySwiper4', {
	navigation: {
	  nextEl: '#bn4',
	  prevEl: '#bp4'
	},
	slidesPerView: 1,
	spaceBetween: 10,
	// init: false,
	pagination: {
	  el: '.swiper-pagination-4',
	  clickable: true,
	},
	breakpoints: {
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