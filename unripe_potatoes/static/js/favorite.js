const favBtns = document.querySelectorAll('.fav-button');

favBtns.forEach(favBtn => {
    favBtn.addEventListener('click', () => {
        fetch('/handle-favorite/?id=' + favBtn.value)
            .then(() => {
                location.reload()
            })
    })
})