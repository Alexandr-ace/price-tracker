function ErrorAlert({ error }) {
  if (!error) return null;
  return (
    <div className="error-alert">
      <i className="fas fa-exclamation-triangle"></i>
      <span>{error}</span>
    </div>
  );
}

export default ErrorAlert;
