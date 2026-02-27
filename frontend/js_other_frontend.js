// Получаем элементы
const urlInput = document.getElementById("urlInput");
const sendBtn = document.getElementById("parseButton");
const statusInput = document.getElementById("status");
const errorInput = document.getElementById("errorAlert");
const errorText = document.getElementById("errorText"); // не использовался, но добавим для полноты

// Шаблоны строк
const templateRow = document.querySelector(".product-row"); // для категорий
const templateRowSingle = document.querySelector(".product-row-single"); // для одного товара

// Контейнеры для вставки строк
const containerCategories = document.getElementById("container-categories");
const containerSingle = document.getElementById("container-single");

// Карточки (блоки с таблицами)
const categoryCard = document.querySelector(".results-card.categories");
const singleCard = document.querySelector(".results-card.single");

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

sendBtn.addEventListener("click", async () => {
  // Скрываем старые ошибки и показываем статус
  errorInput.classList.add("hidden");
  statusInput.classList.remove("hidden");

  // Очищаем предыдущие строки (кроме заголовков)
  document
    .querySelectorAll(".product-row:not(.header)")
    .forEach((row) => row.remove());
  document
    .querySelectorAll(".product-row-single:not(.header)")
    .forEach((row) => row.remove());

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

    // Проверяем структуру ответа
    if (!Array.isArray(data) || data.length < 2) {
      throw new Error("Некорректный формат ответа от сервера");
    }

    const type = data[0]; // 'category' или 'product'
    const products = data[1]; // массив товаров

    console.log(`Тип страницы: ${type}`);
    console.log("Товары (products):", products);
    console.log("products является массивом?", Array.isArray(products));

    if (!Array.isArray(products)) {
      throw new Error("Данные товаров не являются массивом");
    }

    // Скрываем обе карточки на всякий случай
    categoryCard.classList.add("hidden");
    singleCard.classList.add("hidden");

    if (type === "category") {
      // Показываем карточку категорий
      categoryCard.classList.remove("hidden");

      products.forEach((product, index) => {
        try {
          if (!templateRow) throw new Error("Шаблон для категорий не найден");

          const row = templateRow.cloneNode(true);
          // Заполняем ячейки
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
    } else if (type === "product") {
      // Показываем карточку одного товара
      singleCard.classList.remove("hidden");

      products.forEach((product, index) => {
        try {
          if (!templateRowSingle)
            throw new Error("Шаблон для одного товара не найден");

          const row = templateRowSingle.cloneNode(true);
          // Заполняем ячейки для одного товара (7 полей)
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
      throw new Error(`Неизвестный тип страницы: ${type}`);
    }

    statusInput.classList.add("hidden");
  } catch (error) {
    console.error("Перехвачена ошибка:", error);
    statusInput.classList.add("hidden");
    if (errorText) errorText.textContent = error.message;
    errorInput.classList.remove("hidden");
  }
});
