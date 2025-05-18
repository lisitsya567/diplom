const swiper = new Swiper('.profile-cards', {
    direction: 'horizontal',
    slidesPerView: 'auto',
    spaceBetween: 20,
    slidesPerGroup: 1,
    speed: 800,
    loop: false,
    watchOverflow: true,
    allowTouchMove: true,
    centeredSlides: false,
    navigation: {
      nextEl: '.profile-slider-btn-next',
      prevEl: '.profile-slider-btn-prev',
    },
    mousewheel: true,
    breakpoints: {
      768: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      1024: {
        slidesPerView: 'auto',
        spaceBetween: 20,
      }
    }
});


