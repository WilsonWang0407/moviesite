//swiper 
var swiper = new Swiper(".v-list-content", {
    slidesPerView: 1,
    spaceBetween: 1,
    autoplay: {
      delay: 755500,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints:{
        280:{
            slidesPerView: 1,
            spaceBetween: 10,
        },
        320:{
            slidesPerView: 1,
            spaceBetween: 10,
        },
        540:{
            slidesPerView: 1,
            spaceBetween: 10,
        },
        758:{
            slidesPerView: 2,
            spaceBetween: 15,
        },
        900:{
            slidesPerView: 3,
            spaceBetween: 10,
        },
        1365: {
            slidesPerView: 4,
            spaceBetween: 10,
        },
        1600: {
            slidesPerView: 5,
            spaceBetween: 10,
        }
    },
});