const card2 = document.querySelector('.card2');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');


const cards = document.querySelectorAll('.animate-on-scroll');


let index = 0;

const cardWidth = 300;
const visibleComm = 4;

nextBtn.addEventListener('click', () => {
    if (index < card2.children.length - visibleComm) {
        index++;
    } else {
        index = 0
    }
    updateSlider();
});

prevBtn.addEventListener('click', () => {
    if (index > 0) {
        index--;
    } else {
        index = card2.children.length - visibleComm;
    }
    updateSlider();
});

function updateSlider() {
    const cardNew = -index * cardWidth;
    card2.style.transform = `translateX(${cardNew}px)`;
}





// АНИМАЦИЯ КАРТОЧЕК НАПРАВЛЕНИЙ СПЕЦИАОЛЬНОСТЕЙ 


const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Убираем, чтобы не анимировалось повторно
      }
    });
  }, {
    threshold: 0.1
  });

  cards.forEach(card => {
    observer.observe(card);
  });



// Яндекс карта 

// ymaps.ready(function () {
//     var myMap = new ymaps.Map("yandex-map", {
//         center: [55.751574, 37.573856], // Координаты центра
//         zoom: 10, // Уровень масштабирования
//         type: "yandex#map", // Обычная карта (можно заменить на yandex#satellite)
//         controls: ["zoomControl"] // Оставляем только кнопки зума
//     });

//     // Устанавливаем темную карту
//     myMap.setType("yandex#dark");
// });


