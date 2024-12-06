document.getElementById('search-input').addEventListener('input', function() {
    var input = this.value;
    if (input.length >= 3) {
        fetch('/search-suggestions/?q=' + input)
            .then(response => response.json())
            .then(data => {
                var suggestionsList = document.getElementById('suggestions-list');
                suggestionsList.innerHTML = '';
                data.names.forEach(function(item) {
                    var li = document.createElement('li');
                    li.textContent = item;
                    li.addEventListener('click', function() {
                        i = data.names.indexOf(item)
                        window.location.href = `/movie/${data.id[i]}`
                    })
                    suggestionsList.appendChild(li);
                });
            });
    } else {
        var suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = '';
    }
});

document.getElementById('mobsearch-input').addEventListener('input', function() {
    var input = this.value;
    if (input.length >= 3) {
        fetch('/search-suggestions/?q=' + input)
            .then(response => response.json())
            .then(data => {
                var suggestionsList = document.getElementById('mobsuggestions-list');
                suggestionsList.innerHTML = '';
                data.names.forEach(function(item) {
                    var li = document.createElement('li');
                    li.textContent = item;
                    li.addEventListener('click', function() {
                        i = data.names.indexOf(item)
                        window.location.href = `/movie/${data.id[i]}`
                    })
                    suggestionsList.appendChild(li);
                });
            });
    } else {
        var suggestionsList = document.getElementById('mobsuggestions-list');
        suggestionsList.innerHTML = '';
    }
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

function myFunction() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}