function SingleProductRow({ product, index }) {
  const availability =
    product[5] === "in_stock" ? "В наличии" : "Нет в наличии";
  const rating = parseFloat(product[4]);
  const ratingDisplay = isNaN(rating) ? "—" : rating.toFixed(1);
  const date = product[6] || new Date().toLocaleDateString("ru-RU");

  return (
    <div className="grid-row-single product-row-single">
      <div className="product-id">{index + 1}</div>
      <div className="product-title">{product[1] || "—"}</div>
      <div className="product-price">{product[2] || "—"}</div>
      <div className="product-price-notc">{product[3] || "—"}</div>
      <div className="product-rating">{ratingDisplay}</div>
      <div className="product-availability">{availability}</div>
      <div className="product-date">{date}</div>
    </div>
  );
}

function SingleProductTable({ products }) {
  return (
    <div className="results-card single">
      <div className="results-grid" id="container-single">
        {/* Заголовок */}
        <div className="grid-row-single header">
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
            <i className="fas fa-tag"></i> Цена(без О.Б)
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
          <SingleProductRow key={index} product={product} index={index} />
        ))}
      </div>
    </div>
  );
}

export default SingleProductTable;
