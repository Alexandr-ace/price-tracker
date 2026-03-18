function Status({ loading }) {
  if (!loading) return null;
  return (
    <div className="status-section">
      <div className="status">
        <i className="fas fa-spinner fa-spin"></i>
        <span>Идет парсинг...</span>
      </div>
    </div>
  );
}

export default Status;
