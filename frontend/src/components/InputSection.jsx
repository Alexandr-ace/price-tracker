import { useState } from "react";

function InputSection({ onParse }) {
  const [inputValue, setInputValue] = useState("");

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleClear = () => {
    setInputValue("");
    // Можно также убрать фокус, но необязательно
  };

  const handleSubmit = (e) => {
    e.preventDefault(); // предотвращаем перезагрузку страницы, если кнопка внутри формы
    if (inputValue.trim()) {
      onParse(inputValue.trim());
    } else {
      alert("Введите URL");
    }
  };

  return (
    <div className="input-section">
      <div className="url-input-group">
        <i className="fas fa-link icon"></i>
        <input
          id="urlInput"
          type="url"
          value={inputValue}
          onChange={handleChange}
          placeholder="https://example.com"
          required
        />
        {inputValue && (
          <i
            className="fas fa-times-circle icon"
            onClick={handleClear}
            style={{ cursor: "pointer" }}
          ></i>
        )}
        <button id="parseButton" className="btn-parse" onClick={handleSubmit}>
          <i className="fas fa-play"></i> Парсить
        </button>
      </div>
      <p className="hint">
        Попробуйте:
        https://www.ozon.ru/category/aksessuary-7697/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=шапки+мужские+зимние
      </p>
    </div>
  );
}

export default InputSection;
