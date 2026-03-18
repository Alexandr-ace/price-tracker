function TipsBox() {
  return (
    <div className="tips-box">
      <h3>
        <i className="fas fa-lightbulb"></i> Быстрые действия
      </h3>
      <ul className="tips-list">
        <li>
          <span className="tip-highlight">Очистка</span> — удаляет ценовые
          выбросы (IQR)
        </li>
        <li>
          <span className="tip-highlight">Большее/Меньшее</span> — показывает
          товар с экстремальной ценой
        </li>
        <li>
          <span className="tip-highlight">Среднее</span> — вычисляет среднюю
          цену
        </li>
        <li>
          <span className="tip-highlight">Назад</span> — возвращает полный
          список
        </li>
        <li>
          <span className="tip-highlight">Excel-файл</span> — скоро
        </li>
      </ul>
    </div>
  );
}

export default TipsBox;
