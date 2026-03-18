function ButtonPanel({ onClear, onHigh, onLow, onAverage, onBack, onExport }) {
  return (
    <div className="button-section">
      <button className="btn-middle" onClick={onClear}>
        Очистка
      </button>
      <button className="btn-middle" onClick={onHigh}>
        Большее
      </button>
      <button className="btn-middle" onClick={onAverage}>
        Среднее
      </button>
      <button className="btn-middle" onClick={onLow}>
        Меньшее
      </button>
      <button className="btn-middle" onClick={onBack}>
        Назад
      </button>
      <button className="btn-middle" onClick={onExport}>
        Excel-файл
      </button>
    </div>
  );
}

export default ButtonPanel;
