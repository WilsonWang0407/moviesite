document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('ratingInput');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = parseInt(this.getAttribute('data-value'));
            ratingInput.value = value;
            highlightStars(value);
        });
        star.addEventListener('mouseenter', function() {
            const value = parseInt(this.getAttribute('data-value'));
            highlightStars(value);
        });
        star.addEventListener('mouseleave', function() {
            highlightStars(ratingInput.value);
        });
    });

    function highlightStars(value) {
        stars.forEach(star => {
            const starValue = parseInt(star.getAttribute('data-value'));
            if (starValue <= value) {
                star.style.color = '#661b1c';
            } else {
                star.style.color = '#38405F';
            }
        });
        let display = document.querySelector(".modal form .stars .display");
        display.innerHTML = `${value} / 10`;
    }
});