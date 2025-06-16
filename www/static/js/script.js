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

// Поиск врача в форме отзыва
if (window.reviewDoctors) {
    const input = document.getElementById('doctor_search');
    const results = document.getElementById('doctor_search_results');
    const hiddenId = document.getElementById('doctor_id');
    input.addEventListener('input', function() {
        const val = input.value.trim().toLowerCase();
        results.innerHTML = '';
        if (!val) {
            hiddenId.value = '';
            results.style.display = 'none';
            return;
        }
        const matches = window.reviewDoctors.filter(d => d.name.toLowerCase().includes(val));
        if (matches.length === 0) {
            results.style.display = 'none';
            hiddenId.value = '';
            return;
        }
        results.style.display = 'block';
        matches.forEach(d => {
            const div = document.createElement('div');
            div.className = 'search-result-item';
            div.textContent = d.name;
            div.onclick = () => {
                input.value = d.name;
                hiddenId.value = d.id;
                results.style.display = 'none';
            };
            results.appendChild(div);
        });
    });
    // Скрывать выпадающее при клике вне
    document.addEventListener('click', function(e) {
        if (!results.contains(e.target) && e.target !== input) {
            results.style.display = 'none';
        }
    });
}

// Бургер-меню для мобильных 
document.addEventListener('DOMContentLoaded', function() {
  const burger = document.getElementById('burger-menu');
  const nav = document.getElementById('main-nav');
  const body = document.body;
  
  if (burger && nav) {
    burger.addEventListener('click', function() {
      nav.classList.toggle('open');
      burger.classList.toggle('open');
      body.classList.toggle('menu-open');
    });
    
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('open');
        burger.classList.remove('open');
        body.classList.remove('menu-open');
      });
    });
  }
});


