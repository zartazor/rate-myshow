const themeToggle = document.getElementById("theme-toggle");
const root = document.documentElement;
const storedTheme = localStorage.getItem("theme");

if (storedTheme) {
    root.setAttribute("data-theme", storedTheme);
}

themeToggle?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
});

const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");
let searchTimeout;

function renderResults(items) {
    if (!items.length) {
        searchResults.style.display = "none";
        searchResults.innerHTML = "";
        return;
    }

    const html = items
        .slice(0, 6)
        .map(
            (item) =>
                `<a href="/titles/${item.imdbID}/">${item.Title} (${item.Year})</a>`
        )
        .join("");

    searchResults.innerHTML = html;
    searchResults.style.display = "block";
}

searchInput?.addEventListener("input", (event) => {
    const value = event.target.value.trim();
    clearTimeout(searchTimeout);

    if (!value) {
        renderResults([]);
        return;
    }

    searchTimeout = setTimeout(async () => {
        const response = await fetch(`/search/?q=${encodeURIComponent(value)}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
        });
        const data = await response.json();
        renderResults(data.results || []);
    }, 300);
});

window.addEventListener("click", (event) => {
    if (!searchResults.contains(event.target) && event.target !== searchInput) {
        searchResults.style.display = "none";
    }
});

const loadMoreButton = document.getElementById("load-more");
const searchGrid = document.getElementById("search-grid");

loadMoreButton?.addEventListener("click", async () => {
    const query = loadMoreButton.dataset.query;
    const nextPage = parseInt(loadMoreButton.dataset.page || "1", 10) + 1;

    const response = await fetch(`/search/?q=${encodeURIComponent(query)}&page=${nextPage}`, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
    });
    const data = await response.json();

    if (!data.results || data.results.length === 0) {
        loadMoreButton.disabled = true;
        loadMoreButton.textContent = "No more results";
        return;
    }

    const html = data.results
        .map(
            (item) =>
                `<a class="card" href="/titles/${item.imdbID}/">
                    <img src="${item.Poster}" alt="${item.Title}" />
                    <div class="card-body">
                        <h3>${item.Title}</h3>
                        <p>${item.Year}</p>
                    </div>
                </a>`
        )
        .join("");

    searchGrid?.insertAdjacentHTML("beforeend", html);
    loadMoreButton.dataset.page = String(nextPage);
});

const scoreDisplay = document.getElementById("score-display");
const scoreRadios = document.querySelectorAll(".star-rating input[name='score']");

scoreRadios.forEach((radio) => {
    radio.addEventListener("change", () => {
        if (scoreDisplay) {
            scoreDisplay.textContent = `${radio.value} / 10`;
        }
    });
});

const selectedScore = document.querySelector(".star-rating input[name='score']:checked");
if (scoreDisplay && selectedScore) {
    scoreDisplay.textContent = `${selectedScore.value} / 10`;
}
