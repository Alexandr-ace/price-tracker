function CategoryRow({ product, index }) {
  const availability =
    product[4] === "in_stock" ? "В наличии" : "Нет в наличии";
  const rating = parseFloat(product[3]);
  const ratingDisplay = isNaN(rating) ? "—" : rating.toFixed(1);
  const date = product[5] || new Date().toLocaleDateString("ru-RU");

  return (
    <div className="grid-row product-row">
      <div className="product-id">{index + 1}</div>
      <div className="product-title">{product[1] || "—"}</div>
      <div className="product-price">{product[2] || "—"}</div>
      <div className="product-rating">{ratingDisplay}</div>
      <div className="product-availability">{availability}</div>
      <div className="product-date">{date}</div>
    </div>
  );
}

function CategoryTable({ products }) {
  return (
    <div className="results-card categories">
      <div className="results-grid" id="container-categories">
        {/* Заголовок */}
        <div className="grid-row header">
          <div>
            <i className="fas fa-hashtag"></i> ID
          </div>
          <div>
            <i className="fas fa-heading"></i> Название
          </div>
          <div>
            <i className="fas fa-tag"></i> Цена
          </div>
          <div>
            <i className="fas fa-star"></i> Рейтинг
          </div>
          <div>
            <i className="fas fa-box"></i> Наличие
          </div>
          <div>
            <i className="fas fa-calendar-alt"></i> Дата
          </div>
        </div>
        {/* Строки товаров */}
        {products.map((product, index) => (
          <CategoryRow key={index} product={product} index={index} />
        ))}
      </div>
    </div>
  );
}

export default CategoryTable;
