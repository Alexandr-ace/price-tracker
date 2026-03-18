import { useState } from "react";
import InputSection from "./components/InputSection";
import ButtonPanel from "./components/ButtonPanel";
import Status from "./components/Status";
import Results from "./components/Results";
import ErrorAlert from "./components/ErrorAlert";
import TipsBox from "./components/TipsBox";

// Вспомогательная функция извлечения цены
const extractPrice = (product, type) => {
  const priceStr = type === "category" ? product[2] : product[3];
  const digits = priceStr?.replace(/[^\d]/g, "") || "";
  return digits ? parseInt(digits, 10) : 0;
};

// Функция фильтрации выбросов (IQR)
const filterOutliers = (products, type) => {
  if (products.length < 4) return products.slice();

  const prices = products.map((p) => extractPrice(p, type));
  prices.sort((a, b) => a - b);

  const q1 = prices[Math.floor(prices.length * 0.25)];
  const q3 = prices[Math.floor(prices.length * 0.75)];
  const iqr = q3 - q1;
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;

  return products.filter((p) => {
    const price = extractPrice(p, type);
    return price >= lowerBound && price <= upperBound;
  });
};

function App() {
  const [originalProducts, setOriginalProducts] = useState([]);
  const [displayProducts, setDisplayProducts] = useState([]);
  const [currentType, setCurrentType] = useState("");
  const [functionalProducts, setFunctionalProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Парсинг URL
  const handleParse = async (url) => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("http://localhost:8000/parce", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error(
          `Ошибка HTTP: ${response.status} ${response.statusText}`,
        );
      }

      const data = await response.json();
      if (!Array.isArray(data) || data.length < 2) {
        throw new Error("Некорректный формат ответа от сервера");
      }

      const [typeFromServer, productsFromServer] = data;
      if (!Array.isArray(productsFromServer)) {
        throw new Error("Данные товаров не являются массивом");
      }

      setCurrentType(typeFromServer);
      setOriginalProducts(productsFromServer);
      setDisplayProducts(productsFromServer);
      setFunctionalProducts([]); // сбрасываем сохранённые после очистки
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Очистка выбросов
  const handleClearOutliers = () => {
    if (originalProducts.length === 0) {
      setError("Сначала загрузите данные");
      return;
    }
    const beforeCount = originalProducts.length;
    const filtered = filterOutliers(originalProducts, currentType);
    setDisplayProducts(filtered);
    setFunctionalProducts(filtered);
    const removed = beforeCount - filtered.length;
    alert(`После очистки было исключено: ${removed} товаров`);
  };

  // Максимальная цена
  const handleHighPrice = () => {
    if (displayProducts.length === 0) {
      setError("Нет данных для поиска максимума");
      return;
    }
    const maxProduct = displayProducts.reduce((max, p) => {
      const price = extractPrice(p, currentType);
      const maxPrice = max ? extractPrice(max, currentType) : -Infinity;
      return price > maxPrice ? p : max;
    }, null);
    if (maxProduct) setDisplayProducts([maxProduct]);
  };

  // Минимальная цена
  const handleLowPrice = () => {
    if (displayProducts.length === 0) {
      setError("Нет данных для поиска минимума");
      return;
    }
    const minProduct = displayProducts.reduce((min, p) => {
      const price = extractPrice(p, currentType);
      const minPrice = min ? extractPrice(min, currentType) : Infinity;
      return price < minPrice ? p : min;
    }, null);
    if (minProduct) setDisplayProducts([minProduct]);
  };

  // Средняя цена
  const handleAveragePrice = () => {
    if (displayProducts.length === 0) {
      setError("Нет данных для вычисления среднего");
      return;
    }
    const sum = displayProducts.reduce(
      (acc, p) => acc + extractPrice(p, currentType),
      0,
    );
    const avg = sum / displayProducts.length;
    alert(`Средняя цена: ${avg.toFixed(2)} ₽`);
  };

  // Назад
  const handleBack = () => {
    if (originalProducts.length === 0) {
      setError("Нет исходных данных");
      return;
    }
    // Сравниваем длины, как в оригинале
    if (displayProducts.length !== functionalProducts.length) {
      setDisplayProducts(functionalProducts.slice());
    } else if (displayProducts.length !== originalProducts.length) {
      setDisplayProducts(originalProducts.slice());
      setFunctionalProducts(originalProducts.slice());
    }
  };

  // Очистка ошибки через 4 секунды (как в оригинале)
  // Но можно просто показывать и убирать вручную, или добавить эффект
  // Для простоты оставим так: error исчезнет после нового действия или по таймеру
  // Добавим автоматическое скрытие через 4 секунды при появлении ошибки
  const showError = (msg) => {
    setError(msg);
    setTimeout(() => setError(""), 4000);
  };

  // Переопределим setError на showError в нужных местах, но проще пока оставить как есть

  // Реализуем получение Excel файла
  const exportToExcel = () => {
    if (displayProducts.length === 0) {
      alert("Нет данных для экспорта");
      return;
    }

    // Формируем HTML-таблицу
    let html = '<table border="1" style="border-collapse: collapse;">';

    // Определяем заголовки в зависимости от типа
    if (currentType === "category") {
      html +=
        "<thead><tr>" +
        "<th>ID</th>" +
        "<th>Название</th>" +
        "<th>Цена</th>" +
        "<th>Рейтинг</th>" +
        "<th>Наличие</th>" +
        "<th>Дата</th>" +
        "</tr></thead><tbody>";

      displayProducts.forEach((p, idx) => {
        const availability =
          p[4] === "in_stock" ? "В наличии" : "Нет в наличии";
        const rating = !isNaN(parseFloat(p[3]))
          ? parseFloat(p[3]).toFixed(1)
          : "—";
        const date = p[5] || new Date().toLocaleDateString("ru-RU");
        html += `<tr>
        <td>${idx + 1}</td>
        <td>${p[1] || ""}</td>
        <td>${p[2] || ""}</td>
        <td>${rating}</td>
        <td>${availability}</td>
        <td>${date}</td>
      </tr>`;
      });
    } else if (currentType === "product") {
      html +=
        "<thead><tr>" +
        "<th>ID</th>" +
        "<th>Название</th>" +
        "<th>Цена</th>" +
        "<th>Цена(без О.Б)</th>" +
        "<th>Рейтинг</th>" +
        "<th>Наличие</th>" +
        "<th>Дата</th>" +
        "</tr></thead><tbody>";

      displayProducts.forEach((p, idx) => {
        const availability =
          p[5] === "in_stock" ? "В наличии" : "Нет в наличии";
        const rating = !isNaN(parseFloat(p[4]))
          ? parseFloat(p[4]).toFixed(1)
          : "—";
        const date = p[6] || new Date().toLocaleDateString("ru-RU");
        html += `<tr>
        <td>${idx + 1}</td>
        <td>${p[1] || ""}</td>
        <td>${p[2] || ""}</td>
        <td>${p[3] || ""}</td>
        <td>${rating}</td>
        <td>${availability}</td>
        <td>${date}</td>
      </tr>`;
      });
    } else {
      return;
    }

    html += "</tbody></table>";

    // Добавляем базовую HTML-структуру с указанием кодировки
    const fullHtml = `
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Экспорт цен</title>
      </head>
      <body>
        ${html}
      </body>
    </html>
  `;

    const blob = new Blob([fullHtml], { type: "application/vnd.ms-excel" }); // важно: тип для Excel
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.setAttribute("download", "prices.xls"); // расширение .xls
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container">
      <main>
        <InputSection onParse={handleParse} />
        <ButtonPanel
          onClear={handleClearOutliers}
          onHigh={handleHighPrice}
          onLow={handleLowPrice}
          onAverage={handleAveragePrice}
          onBack={handleBack}
          onExport={exportToExcel}
        />
        <Status loading={loading} />
        <Results products={displayProducts} type={currentType} />
        <ErrorAlert error={error} />
        <TipsBox />
      </main>
    </div>
  );
}

export default App;
