const API_URL = "/api/movies";

const form = document.getElementById("movie-form");
const moviesContainer = document.getElementById("movies");


async function loadMovies() {
    const response = await fetch(API_URL);
    const movies = await response.json();

    moviesContainer.innerHTML = "";

    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";

        card.innerHTML = `
            <h3>${movie.title}</h3>
            <p class="genre">${movie.genre || "Жанр не указан"}</p>

            <p class="rating rating-${movie.rating}">
                ★ ${movie.rating || "—"}/10
            </p>

            <span class="status">
                ${movie.status || "Без статуса"}
            </span>
        `;

        moviesContainer.appendChild(card);
    });
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const movie = {
        title: document.getElementById("title").value,
        genre: document.getElementById("genre").value,
        rating: document.getElementById("rating").value || null,
        status: document.getElementById("status").value
    };

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(movie)
    });

    form.reset();

    await loadMovies();
});


loadMovies();