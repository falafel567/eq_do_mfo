const filterForm = document.getElementById('filter-form');
const container = document.getElementById('results-container');

function fetchData(params) {
    fetch('/?' + params.toString(), {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(r => r.text())
    .then(html => {
        container.innerHTML = html;
        window.history.replaceState(null, '', '?' + params.toString());
    });
}

// Obsługa wyszukiwania
filterForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const params = new URLSearchParams(new FormData(this));
    params.set('page', 1); // Resetuj do 1 strony przy nowym szukaniu
    fetchData(params);
});

// Obsługa klikania w strony (Delegacja zdarzeń)
container.addEventListener('click', function(e) {
    if (e.target.classList.contains('page-link')) {
        const page = e.target.getAttribute('data-page');
        const params = new URLSearchParams(new FormData(filterForm));
        params.set('page', page);
        fetchData(params);
    }
});

const resetBtn = document.getElementById('reset-btn');

resetBtn.addEventListener('click', function() {
    // 1. Czyścimy formularz
    filterForm.reset();

    // 2. Tworzymy puste parametry (pokażą wszystkie przedmioty)
    const params = new URLSearchParams();

    // 3. Wywołujemy funkcję pobierania danych z pustymi parametrami
    fetchData(params);
});