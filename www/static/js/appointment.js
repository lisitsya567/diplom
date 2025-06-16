document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('appointmentForm');
    const dateInput = document.getElementById('date');
    const timeSelect = document.getElementById('time');
    const doctorIdInput = document.getElementById('doctorId');
    
    // Устанавливаем минимальную дату (седня)
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
    
    // Обработчик изменения даты
    dateInput.addEventListener('change', async function() {
        const date = this.value;
        const doctorId = doctorIdInput.value;
        
        if (date && doctorId) {
            try {
                const response = await fetch(`/api/available-times?doctor_id=${doctorId}&date=${date}`);
                const times = await response.json();
                
                // Получаем текущее время по мск
                const now = new Date();
                const moscowOffset = 3 * 60; // Москва UTC+3
                const localOffset = now.getTimezoneOffset();
                const moscowNow = new Date(now.getTime() + (moscowOffset + localOffset) * 60000);
                const moscowHours = moscowNow.getHours();
                const moscowMinutes = moscowNow.getMinutes();
                
                // Очищаем и заполняем select
                timeSelect.innerHTML = '';
                times.forEach(time => {
                    const option = document.createElement('option');
                    option.value = time;
                    option.textContent = time;
                    // Если выбран сегодня, скрываем прошедшие слоты
                    if (date === moscowNow.toISOString().slice(0,10)) {
                        const [h, m] = time.split(':').map(Number);
                        if (h < moscowHours || (h === moscowHours && m <= moscowMinutes)) {
                            option.disabled = true;
                            option.style.display = 'none';
                        }
                    }
                    timeSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Ошибка при получении доступного времени:', error);
            }
        }
    });
    
    // Обработчик отправки формы
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const isGuest = !formData.has('userId'); // Проверяем, гость ли пользователь
        
        try {
            const response = await fetch(isGuest ? '/api/guest-appointment' : '/api/appointment', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                alert('Запись успешно создана!');
                window.location.href = '/'; // Перенаправляем на главную
            } else {
                alert(result.detail || 'Произошла ошибка при создании записи');
            }
        } catch (error) {
            console.error('Ошибка при отправке формы:', error);
            alert('Произошла ошибка при отправке формы');
        }
    });
}); 