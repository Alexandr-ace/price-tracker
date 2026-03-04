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
const errorText = document.getElementById("errorText"); // не использовался, но добавим для полноты
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

let currentProducts = []; // массив товаров (для категории или истории одного товара)
let currentType = ""; // 'category' или 'product'
let functionlProducts = []; // копия исходных данных, чтобы можно было сбросить фильтры

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

// Если шаблоны найдены, удалим их из DOM, чтобы они не отображались
if (templateRow) templateRow.remove();
if (templateRowSingle) templateRowSingle.remove();

// Функция, которая обновляет видимость крестика
function toggleClearIcon() {
  if (input.value.trim() !== "") {
    clearIcon.classList.remove("fas-hidden"); // показываем
  } else {
    clearIcon.classList.add("fas-hidden"); // скрываем
  }
}

// Слушаем событие ввода (input) — срабатывает при каждом изменении
input.addEventListener("input", toggleClearIcon);

// Слушаем клик по крестику
clearIcon.addEventListener("click", function () {
  input.value = ""; // очищаем поле
  input.focus(); // возвращаем фокус (опционально)
  toggleClearIcon(); // скрываем крестик (можно и просто add('fas-hidden'), но лучше вызвать функцию)
});

// При загрузке страницы проверяем, есть ли уже значение (например, если поле не пустое)
toggleClearIcon();

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
    functionlProducts.forEach((product, index) => {
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
    functionlProducts.forEach((product, index) => {
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

sendBtn.addEventListener("click", async () => {
  // Скрываем старые ошибки и показываем статус
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

    const currentType = data[0]; // 'category' или 'product'
    const currentProducts = data[1]; // массив товаров

    console.log(`Тип страницы: ${currentType}`);
    console.log("Товары:", currentProducts);

    if (!Array.isArray(currentProducts)) {
      throw new Error("Данные товаров не являются массивом");
    }

    // Сохраняем исходные данные (для будущих кнопок)
    functionlProducts = currentProducts.slice(); // копия
    // Вызываем отрисовку
    renderProducts();

    statusInput.classList.add("hidden");
  } catch (error) {
    console.error("Перехвачена ошибка:", error);
    statusInput.classList.add("hidden");
    if (errorText) errorText.textContent = error.message;
    errorInput.classList.remove("hidden");
  }
});

function filterOutliers() {
  // Если товаров меньше 4, фильтрация бессмысленна
  if (functionlProducts.length < 4) return functionlProducts.slice();

  // Извлекаем цены в числа (удаляем пробелы и символ ₽)
  const prices = functionlProducts.map((p) => {
    const priceStr = currentType === "category" ? p[2] : p[3]; // для истории берём цену без карты (индекс 3)
    return parseFloat(priceStr.replace(/\s/g, "").replace("₽", ""));
  });

  // Сортируем цены
  prices.sort((a, b) => a - b);

  // Вычисляем первый и третий квартили
  const q1 = prices[Math.floor(prices.length * 0.25)];
  const q3 = prices[Math.floor(prices.length * 0.75)];
  const iqr = q3 - q1;
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;

  // Фильтруем исходный массив, оставляя только те товары, цена которых в границах
  functionlProducts = functionlProducts.filter((p) => {
    const price = parseFloat(
      (currentType === "category" ? p[2] : p[3])
        .replace(/\s/g, "")
        .replace("₽", ""),
    );
    return price >= lowerBound && price <= upperBound;
  });

  renderProducts();
}

clearBtn.addEventListener("click", filterOutliers);
