// Получаем элементы
const urlInput = document.getElementById("urlInput");
const sendBtn = document.getElementById("parseButton");
const clearBtn = document.getElementById("clearButton");
const highBtn = document.getElementById("highButton");
const middleBtn = document.getElementById("middleButton");
const lowBtn = document.getElementById("lowButton");
const backBtn = document.getElementById("backButton");
const statusInput = document.getElementById("status");
const errorInput = document.getElementById("errorAlert");
const errorText = document.getElementById("errorText");
const input = document.getElementById("urlInput");
const clearIcon = document.getElementById("clearIcon");

// Шаблоны строк
const templateRow = document.querySelector(".product-row"); // для категорий
const templateRowSingle = document.querySelector(".product-row-single"); // для одного товара

// Контейнеры для вставки строк
const containerCategories = document.getElementById("container-categories");
const containerSingle = document.getElementById("container-single");

// Карточки (блоки с таблицами)
const categoryCard = document.querySelector(".results-card.categories");
const singleCard = document.querySelector(".results-card.single");

// Глобальные переменные состояния
let originalProducts = []; // неизменная копия данных с сервера
let displayProducts = []; // данные, которые сейчас отображаются
let currentType = ""; // 'category' или 'product'

// ========== ПРОВЕРКИ НА ЭТАПЕ ЗАГРУЗКИ ==========
console.log("=== Проверка элементов DOM ===");
console.log("urlInput:", urlInput);
console.log("sendBtn:", sendBtn);
console.log("statusInput:", statusInput);
console.log("errorInput:", errorInput);
console.log("templateRow (категории):", templateRow);
console.log("templateRowSingle (один товар):", templateRowSingle);
console.log("containerCategories:", containerCategories);
console.log("containerSingle:", containerSingle);
console.log("categoryCard:", categoryCard);
console.log("singleCard:", singleCard);

// Удаляем шаблоны из DOM (они больше не нужны как видимые элементы)
if (templateRow) templateRow.remove();
if (templateRowSingle) templateRowSingle.remove();

// ---------- Функция отрисовки (использует глобальные displayProducts и currentType) ----------
function renderProducts() {
  // Очищаем оба контейнера от старых строк (кроме заголовков)
  document
    .querySelectorAll(".product-row:not(.header)")
    .forEach((row) => row.remove());
  document
    .querySelectorAll(".product-row-single:not(.header)")
    .forEach((row) => row.remove());

  // Скрываем обе карточки, потом покажем нужную
  categoryCard.classList.add("hidden");
  singleCard.classList.add("hidden");

  if (currentType === "category") {
    categoryCard.classList.remove("hidden");
    if (!templateRow) {
      console.error("Шаблон для категорий не найден");
      return;
    }
    displayProducts.forEach((product, index) => {
      try {
        const row = templateRow.cloneNode(true);
        row.querySelector(".product-id").textContent = product[0] || "—";
        row.querySelector(".product-title").textContent = product[1] || "—";
        row.querySelector(".product-price").textContent = product[2] || "—";

        const rating = parseFloat(product[3]);
        row.querySelector(".product-rating").textContent = isNaN(rating)
          ? "—"
          : rating.toFixed(1);

        row.querySelector(".product-availability").textContent =
          product[4] === "in_stock" ? "В наличии" : "Нет в наличии";

        row.querySelector(".product-date").textContent =
          product[5] || new Date().toLocaleDateString("ru-RU");

        containerCategories.appendChild(row);
      } catch (err) {
        console.error(
          `Ошибка при обработке товара #${index} (категория):`,
          err,
          product,
        );
      }
    });
  } else if (currentType === "product") {
    singleCard.classList.remove("hidden");
    if (!templateRowSingle) {
      console.error("Шаблон для одного товара не найден");
      return;
    }
    displayProducts.forEach((product, index) => {
      try {
        const row = templateRowSingle.cloneNode(true);
        row.querySelector(".product-id").textContent = product[0] || "—";
        row.querySelector(".product-title").textContent = product[1] || "—";
        row.querySelector(".product-price").textContent = product[2] || "—";
        row.querySelector(".product-price-notc").textContent =
          product[3] || "—";

        const rating = parseFloat(product[4]);
        row.querySelector(".product-rating").textContent = isNaN(rating)
          ? "—"
          : rating.toFixed(1);

        row.querySelector(".product-availability").textContent =
          product[5] === "in_stock" ? "В наличии" : "Нет в наличии";

        row.querySelector(".product-date").textContent =
          product[6] || new Date().toLocaleDateString("ru-RU");

        containerSingle.appendChild(row);
      } catch (err) {
        console.error(
          `Ошибка при обработке товара #${index} (один товар):`,
          err,
          product,
        );
      }
    });
  } else {
    console.error(`Неизвестный тип: ${currentType}`);
  }
}

// ---------- Функция фильтрации выбросов (IQR) ----------
function filterOutliers() {
  if (originalProducts.length < 4) {
    // Если данных мало, просто показываем оригинал
    displayProducts = originalProducts.slice();
    renderProducts();
    return;
  }

  // Извлекаем цены в числа (удаляем пробелы и символ ₽)
  const prices = originalProducts.map((p) => {
    const priceStr = currentType === "category" ? p[2] : p[3];
    return parseFloat(priceStr.replace(/\s/g, "").replace("₽", ""));
  });

  // Сортируем цены
  prices.sort((a, b) => a - b);

  // Квартили
  const q1 = prices[Math.floor(prices.length * 0.25)];
  const q3 = prices[Math.floor(prices.length * 0.75)];
  const iqr = q3 - q1;
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;

  // Фильтруем оригинальный массив
  displayProducts = originalProducts.filter((p) => {
    const price = parseFloat(
      (currentType === "category" ? p[2] : p[3])
        .replace(/\s/g, "")
        .replace("₽", ""),
    );
    return price >= lowerBound && price <= upperBound;
  });

  renderProducts();
}

// ---------- Вспомогательная функция для временных сообщений ----------
function showTemporaryError(message) {
  errorText.textContent = message;
  errorInput.classList.remove("hidden");
  setTimeout(() => errorInput.classList.add("hidden"), 4000);
}

// ---------- Кнопка "Очистить поле ввода" (крестик) ----------
function toggleClearIcon() {
  clearIcon.classList.toggle("fas-hidden", input.value.trim() === "");
}
input.addEventListener("input", toggleClearIcon);
clearIcon.addEventListener("click", () => {
  input.value = "";
  input.focus();
  toggleClearIcon();
});
toggleClearIcon(); // начальное состояние

// ---------- Основной обработчик: парсинг URL ----------
sendBtn.addEventListener("click", async () => {
  errorInput.classList.add("hidden");
  statusInput.classList.remove("hidden");

  const url = urlInput.value.trim();
  if (!url) {
    statusInput.classList.add("hidden");
    errorInput.classList.remove("hidden");
    if (errorText) errorText.textContent = "Введите URL";
    return;
  }

  try {
    console.log("Отправляем запрос на URL:", url);
    const response = await fetch("http://localhost:8000/parce", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    });

    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Ответ от сервера (сырой):", data);

    if (!Array.isArray(data) || data.length < 2) {
      throw new Error("Некорректный формат ответа от сервера");
    }

    const typeFromServer = data[0];
    const productsFromServer = data[1];

    console.log(`Тип страницы: ${typeFromServer}`);
    console.log("Товары:", productsFromServer);

    if (!Array.isArray(productsFromServer)) {
      throw new Error("Данные товаров не являются массивом");
    }

    // Сохраняем глобальные данные
    currentType = typeFromServer;
    originalProducts = productsFromServer.slice(); // копия оригинала
    displayProducts = productsFromServer.slice(); // начинаем с отображения оригинала

    // Отрисовываем
    renderProducts();

    statusInput.classList.add("hidden");
  } catch (error) {
    console.error("Перехвачена ошибка:", error);
    statusInput.classList.add("hidden");
    if (errorText) errorText.textContent = error.message;
    errorInput.classList.remove("hidden");
  }
});

// ---------- Кнопка "Очистить выбросы" (фильтрация) ----------
clearBtn.addEventListener("click", () => {
  if (originalProducts.length === 0) {
    showTemporaryError("Сначала загрузите данные");
    return;
  }
  let beforeFilterOutliers = originalProducts.length;
  filterOutliers();
  let afterFilterOutliers = originalProducts.length;
  let numberGoods = beforeFilterOutliers - afterFilterOutliers;
  alert(`После очистки было исключено: ${numberGoods} товаров`);
});

// ---------- Кнопка "Самое большое" ----------
highBtn.addEventListener("click", () => {
  if (displayProducts.length === 0) {
    showTemporaryError("Нет данных для поиска максимума");
    return;
  }
  let maxProduct = displayProducts.reduce((max, p) => {
    const price = parseFloat(
      (currentType === "category" ? p[2] : p[3])
        .replace(/\s/g, "")
        .replace("₽", ""),
    );
    const maxPrice = max
      ? parseFloat(
          (currentType === "category" ? max[2] : max[3])
            .replace(/\s/g, "")
            .replace("₽", ""),
        )
      : -Infinity;
    return price > maxPrice ? p : max;
  }, null);
  if (maxProduct) {
    displayProducts = [maxProduct];
    renderProducts();
  }
});

// ---------- Кнопка "Самое маленькое" ----------
lowBtn.addEventListener("click", () => {
  if (displayProducts.length === 0) {
    showTemporaryError("Нет данных для поиска минимума");
    return;
  }
  let minProduct = displayProducts.reduce((min, p) => {
    const price = parseFloat(
      (currentType === "category" ? p[2] : p[3])
        .replace(/\s/g, "")
        .replace("₽", ""),
    );
    const minPrice = min
      ? parseFloat(
          (currentType === "category" ? min[2] : min[3])
            .replace(/\s/g, "")
            .replace("₽", ""),
        )
      : Infinity;
    return price < minPrice ? p : min;
  }, null);
  if (minProduct) {
    displayProducts = [minProduct];
    renderProducts();
  }
});

// ---------- Кнопка "Среднее" ----------
middleBtn.addEventListener("click", () => {
  if (displayProducts.length === 0) {
    showTemporaryError("Нет данных для вычисления среднего");
    return;
  }
  let sum = 0;
  displayProducts.forEach((p) => {
    const price = parseFloat(
      (currentType === "category" ? p[2] : p[3])
        .replace(/\s/g, "")
        .replace("₽", ""),
    );
    sum += price;
  });
  const avg = sum / displayProducts.length;
  alert(`Средняя цена: ${avg.toFixed(2)} ₽`);
});

// ---------- Кнопка "Назад" (сброс к исходным данным) ----------
backBtn.addEventListener("click", () => {
  if (originalProducts.length === 0) {
    showTemporaryError("Нет исходных данных");
    return;
  }
  displayProducts = originalProducts.slice();
  renderProducts();
});
