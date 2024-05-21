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

document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".ver-pelicula");

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            // Obtener el nombre de la película
            const movieName = this.parentElement.querySelector(".movie-name").innerText;
            
            // Mostrar el nombre de la película en la consola
            console.log(movieName);
            
            // Cambiar el color del botón
            this.style.backgroundColor = "white";
            this.style.color = "black";

            // Enviar el nombre de la película al servidor
            fetch('/User', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ movie_name: movieName })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

