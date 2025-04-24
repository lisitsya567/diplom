const swiper = new Swiper('.cards-doctors', {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: false, // если нужно бесконечное листание — true
    navigation: {
      nextEl: '.doctor-slider-btn-next',
      prevEl: '.doctor-slider-btn-prev',
    },
    breakpoints: {
      768: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 30,
      }
    }
  });
  

  