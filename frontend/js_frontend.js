document.addEventListener("DOMContentLoaded", function () {
  // Элементы DOM
  const urlInput = document.getElementById("urlInput");
  const parseButton = document.getElementById("parseButton");
  const statusDiv = document.getElementById("status");
  const statusText = document.getElementById("statusText");
  const titleResult = document.getElementById("titleResult");
  const descriptionResult = document.getElementById("descriptionResult");
  const errorAlert = document.getElementById("errorAlert");
  const errorText = document.getElementById("errorText");

  // Базовый URL вашего бэкенда (ИЗМЕНИТЕ НА СВОЙ!)
  // Предполагается, что ваш бэкенд запущен локально на порту 8000
  const API_BASE_URL = "http://localhost:8000";
  // Эндпоинт для парсинга (пример, подставьте свой)
  const PARSE_ENDPOINT = "/parse";

  // Функция для сброса результатов
  function resetResults() {
    titleResult.textContent = "Здесь появится заголовок...";
    titleResult.className = "result-box empty";
    descriptionResult.textContent = "Здесь появится описание...";
    descriptionResult.className = "result-box empty";
    hideError();
  }

  // Функции для отображения/скрытия статуса и ошибок
  function showStatus(message) {
    statusText.textContent = message;
    statusDiv.classList.remove("hidden");
  }

  function hideStatus() {
    statusDiv.classList.add("hidden");
  }

  function showError(message) {
    errorText.textContent = message;
    errorAlert.classList.remove("hidden");
  }

  function hideError() {
    errorAlert.classList.add("hidden");
  }

  // Основная функция парсинга
  async function parseUrl() {
    const url = urlInput.value.trim();

    // Валидация URL
    if (!url) {
      showError("Пожалуйста, введите URL");
      return;
    }

    // Сброс предыдущих результатов
    resetResults();
    showStatus("Идёт загрузка и анализ страницы...");

    try {
      // Отправка запроса на ваш бэкенд
      // Формат запроса зависит от вашего API
      const response = await fetch(`${API_BASE_URL}${PARSE_ENDPOINT}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
      });

      hideStatus();

      if (!response.ok) {
        // Если ответ не ok, пробуем получить текст ошибки
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `Ошибка сервера: ${response.status}`,
        );
      }

      const data = await response.json();

      // Отображение результата
      // Предполагаем, что ваш бэкенд возвращает объект с полями title и description
      if (data.title) {
        titleResult.textContent = data.title;
        titleResult.className = "result-box";
      } else {
        titleResult.textContent = "Заголовок не найден";
        titleResult.className = "result-box empty";
      }

      if (data.description) {
        descriptionResult.textContent = data.description;
        descriptionResult.className = "result-box";
      } else {
        descriptionResult.textContent = "Мета-описание не найдено";
        descriptionResult.className = "result-box empty";
      }
    } catch (error) {
      hideStatus();
      showError(`Не удалось распарсить страницу: ${error.message}`);
      console.error("Ошибка:", error);
    }
  }

  // Обработчики событий
  parseButton.addEventListener("click", parseUrl);
  urlInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      parseUrl();
    }
  });

  // Пример для быстрого тестирования (можно удалить)
  urlInput.addEventListener("focus", function () {
    if (this.value === "") {
      this.value = "https://example.com";
    }
  });

  // Инициализация
  console.log("Фронтенд парсера загружен!");
  console.log("Убедитесь, что бэкенд запущен на", API_BASE_URL);
});
