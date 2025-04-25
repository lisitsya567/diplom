const swiper = new Swiper('.cards-doctors', {
    slidesPerView: 2,   // КОЛ-ВО КАРТОЧЕК ДЛЯ ПОКАЩА НА ЭКРАНЕ
    spaceBetween: 20,  // ОТСТУП ОТ КАРТОЧКИ ПРОБЕЛ
    slidesPerGroup: 1,  // КОЛ-ВО ПРОЛИСТЫВАЕМЫХ КАРТОЧЕК 
    speed: 800, // СКОРОСТЬ ПЕРЕКЛЮЧЕНИЯ КАРТОЧЕК
    // slideToClickedSlide: true, // ПЕРЕКЛЮЧЕНИЕ ПРИ КЛИКЕ НА КАРТОЧКУ 
    loop: false, // БЕСКОНЕЧНОЕ ЛИСТАНИЕ НУЖНО true НЕ ПРОДДЕРДИВАЕТ СКРОЛЛ
    navigation: {
      nextEl: '.doctor-slider-btn-next',
      prevEl: '.doctor-slider-btn-prev',
    },
    breakpoints: {   // АДАПТИВНОСТЬ НАСТРОЕК ПОД МОБИЛЬНЫЕ ЭКРАНЫ
      768: {
        slidesPerView: 1,
        spaceBetween: 20,
        slidesPerGroup: 0.1,
        touchRation: 1, // ЧУВСТВИТЕЛЬНОСТЬ СВАЙПА 
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 45,
        slidesPerGroup: 1,
        slideToClickedSlide: true,  
      }
    }
  });
  

  