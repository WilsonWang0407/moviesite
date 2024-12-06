const data = document.currentScript.dataset;
const movieData = JSON.parse(data.movies);

function getFilterList() {
    let genreCheckBoxes = document.getElementsByClassName('btn-check');
    let filters = [];

    for (let genreCheckBox of genreCheckBoxes) {
        if (genreCheckBox.checked === true) {
            filters.push(genreCheckBox.value);
        }
    }

    return filters;
}

function createMovieList(moviesToShow, currentPage, pageSize) {

    let maxNumPage = Math.ceil(moviesToShow.length / pageSize);

    let maxMovie = currentPage * pageSize;
    if (maxMovie > moviesToShow.length) maxMovie = moviesToShow.length;
    
    let numBtns = 5;

    let minBtn = currentPage;
    
    if (currentPage == 1) minBtn = currentPage;
    else if (currentPage == 2) minBtn = currentPage - 1;
    else if (currentPage > 2) minBtn = currentPage - 2;
    else if (currentPage > (maxNumPage - numBtns)) minBtn = maxNumPage - numBtns;
    
    if (maxNumPage < numBtns){ 
        numBtns = maxNumPage;
        minBtn = 1;
    }

    movieInfo = `<div class="movie-list-info"><p>Showing ${(currentPage - 1) * pageSize + 1} - ${maxMovie} of ${moviesToShow.length}</p></div>`;
    movies = '';
    pagination = `<nav aria-label="Page navigation">
                    <ul class="pagination pagination-lg">
                        <li class="page-item">
                            <a class="page-link" aria-label="First" onclick="createMovieList(1, ${pageSize})">
                                <span aria-hidden="true">First</span>
                            </a>
                        </li>`;

    if (currentPage > 1) {
        pagination += `<li class="page-item">
                            <a class="page-link" aria-label="Previous" onclick="createMovieList(${currentPage - 1}, ${pageSize})">
                                <span aria-hidden="true">Previous</span>
                            </a>
                        </li>`;
    } else {
        pagination += `<li class="page-item">
                            <a class="page-link" aria-label="Previous" disabled>
                                <span aria-hidden="true">Previous</span>
                            </a>
                        </li>`;
    }

    for (let i = ((currentPage - 1) * pageSize); i < maxMovie; i++) {
        
        movies += `<div class="movie-item">
                        <a class="movie-item-link" href="/movie/${ moviesToShow[i].id }">
                            <img class="movie-item-img" src="${ moviesToShow[i].thumbnail }" alt="${ moviesToShow[i].name }">
                            <div class="movie-info">
                                <h3>${ moviesToShow[i].name }</h3>
                                <p>${ moviesToShow[i].year }</p>
                                <p>${ moviesToShow[i].genre }</p>
                                <p>${ moviesToShow[i].rating } / 10</p>
                                <p>${ moviesToShow[i].loggedIn === true ? 
                                    moviesToShow[i].favorite === true ? 
                                    `<button class="btn btn-link fav-button" data-bs-toggle="tooltip" data-bs-placement="top" title="Remove from favorites" value=${moviesToShow[i].id}>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="1.5rem" height="1.5rem" fill="#661b1c" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"></path>
                                        </svg>
                                    </button>`    :
                                    `<button class="btn btn-link fav-button" data-bs-toggle="tooltip" data-bs-placement="top" title="Add to favorites" value=${moviesToShow[i].id}>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="1.5rem" height="1.5rem" fill="#661b1c" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"></path>
                                        </svg>
                                    </button>` :
                                    '' 
                                }</p>
                            </div>
                        </a>
                    </div>`;
    }

    for (let i = minBtn; i < (minBtn + numBtns); i++) {
        if (i == currentPage) pagination += `<li class="page-item"><a class="page-link active">${i}</a></li>`
        else pagination += `<li class="page-item"><a class="page-link" onclick="createMovieList(${i}, ${pageSize})">${i}</a></li>`
    }

    if (currentPage < maxNumPage) {
        pagination += `<li class="page-item">
                            <a class="page-link" aria-label="Next" onclick="createMovieList(${currentPage + 1}, ${pageSize})">
                                <span aria-hidden="true">Next</span>
                            </a>
                        </li>`
        } else {
            pagination += `<li class="page-item">
                                <a class="page-link" aria-label="Next" disabled>
                                    <span aria-hidden="true">Next</span>
                                </a>
                            </li>`;
        }
    pagination += `<li class="page-item">
                        <a class="page-link" aria-label="Last" onclick="createMovieList(${maxNumPage}, ${pageSize})">
                            <span aria-hidden="true">Last</span>
                        </a>
                    </li>
                </ul>
            </nav>`;

    document.getElementById('movie-list').innerHTML = movieInfo + movies + pagination;
    window.scrollTo(0, 0);
}

function updateMoviesList(sort='id asc') {
    let moviesToShow = [];
    let filters = getFilterList();

    for (let genre of filters) {
        moviesToShow = moviesToShow.concat(movieData.filter(function(movie) {
            return movie.genre.includes(genre)
        }))
    }

    if (moviesToShow.length === 0) moviesToShow = movieData
    else moviesToShow = Array.from(new Set(moviesToShow))

    let sort_list = sort.split(' ');
    let sortBy = sort_list[0];
    let sortOrder = sort_list[1];
    
    if (sortBy === 'id') {
        moviesToShow.sort(sortById);
        document.getElementById('sort-clear-btn').setAttribute('disabled', true);
    }
    if (sortBy === 'name') {
        moviesToShow.sort(sortByName);
        document.getElementById('sort-clear-btn').removeAttribute('disabled');
    }
    if (sortBy === 'year') {
        moviesToShow.sort(sortByYear);
        document.getElementById('sort-clear-btn').removeAttribute('disabled');
    }
    if (sortBy === 'runtime') {
        moviesToShow.sort(sortByRuntime);
        document.getElementById('sort-clear-btn').removeAttribute('disabled');
    }

    if (sortOrder === 'desc') moviesToShow.reverse();

    createMovieList(moviesToShow, 1, 12);
}

function sortById(movie1, movie2) {
    return movie1.id - movie2.id
}

function sortByYear(movie1, movie2) {
    return movie1.year - movie2.year
}

function sortByName(movie1, movie2) {
    let name1 = movie1.name.toLowerCase();
    let name2 = movie2.name.toLowerCase();

    if (name1 < name2) {
        return -1;
    }
    if (name1 > name2) {
        return 1;
    }
    return 0;
}

function sortByRuntime(movie1, movie2) {
    let runtime1 = parseInt(movie1.runtime.split(' ')[0])
    let runtime2 = parseInt(movie2.runtime.split(' ')[0])
    return runtime1 - runtime2
}

document.getElementById('movie-sort').addEventListener('change', function() {
    let sort = document.getElementById('movie-sort').value;
    updateMoviesList(sort);
});

document.getElementById('sort-clear-btn').addEventListener('click', function() {
    let sort = document.getElementById('movie-sort')
    let event = new Event('change');
    sort.value = 'id asc';
    sort.dispatchEvent(event);
});

let genreCheckBoxes = document.getElementsByClassName('btn-check');

for (let genreCheckBox of genreCheckBoxes) {
    genreCheckBox.addEventListener('click', function() {
        let sort = document.getElementById('movie-sort').value;
        updateMoviesList(sort);
    })
}

createMovieList(movieData, 1, 12);