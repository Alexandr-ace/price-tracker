import CategoryTable from "./CategoryTable";
import SingleProductTable from "./SingleProductTable";

function Results({ products, type }) {
  if (!products.length) return null; // можно показывать заглушку, но по желанию

  return (
    <div className="results-section">
      <h2>
        <i className="fas fa-poll"></i> Результаты
      </h2>
      {type === "category" && <CategoryTable products={products} />}
      {type === "product" && <SingleProductTable products={products} />}
    </div>
  );
}

export default Results;
