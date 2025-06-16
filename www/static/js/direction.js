const swiper = new Swiper('.cards-doctors', {
  slidesPerView: 2,
  spaceBetween: 20,
  slidesPerGroup: 1,
  loop: false,
  speed: 800,
  navigation: {
    nextEl: '.doctor-slider-btn-next',
    prevEl: '.doctor-slider-btn-prev',
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
      spaceBetween: 15,
      slidesPerGroup: 1,
      touchRatio: 1,
    },
    768: {
      slidesPerView: 2,
      spaceBetween: 20,
      slidesPerGroup: 1,
    },
    1024: {
      slidesPerView: 3,
      spaceBetween: 30,
      slidesPerGroup: 1,
    }
  }
});
