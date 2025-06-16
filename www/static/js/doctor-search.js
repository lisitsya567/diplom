document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('doctor-search');
    const searchResults = document.getElementById('search-results');
    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(() => {
            fetch(`/api/search-doctors?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(doctors => {
                    searchResults.innerHTML = '';
                    if (doctors.length > 0) {
                        doctors.forEach(doctor => {
                            const div = document.createElement('div');
                            div.className = 'search-result-item';
                            div.innerHTML = `
                                <div class="doctor-name">${doctor.lname} ${doctor.fname}</div>
                                <div class="doctor-specialization">${doctor.specialization}</div>
                            `;
                            div.addEventListener('click', () => {
                                window.location.href = `/appointment/book/${doctor.id}`;
                            });
                            searchResults.appendChild(div);
                        });
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div class="no-results">Врачи не найдены</div>';
                        searchResults.style.display = 'block';
                    }
                });
        }, 300);
    });

    // Закрытие результатов при клике вне поиска
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}); 