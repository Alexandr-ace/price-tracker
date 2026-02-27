from ozon_parser_test import one_single_product, main_category_product


class DataManager:
    def __init__(self):
        self.single_db = 'parce_base_single.db'
        self.many_db = 'parce_base.db'

    def save_single_product(self, product_data: dict, url: str) -> bool:
        """Сохраняет один товар, используя ВАШ существующий код"""
        # Временно вызываем вашу функцию
        one_single_product(product_data)
        # Но уже логируем URL для будущего использования
        print(f"🔗 URL товара: {url}")

    def save_category_products(self, category_name: str, products: list) -> bool:
        """Сохраняет список товаров"""
        main_category_product(category_name, products)
        return True
