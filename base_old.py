import sqlite3
from datetime import date
# Если таблица сегодня существует, значит мы ее полностью перезаписываем
# Но если стоит другое число, значит создаём новую, а струю сохраняем
# Тестируем


def main_category(table_suffix, cr):
    """Создает таблицу tasks с указанным суффиксом"""
    table_name = f"tasks{table_suffix}"

    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()

    # Создаем таблицу (без лишней запятой в конце)
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price TEXT NOT NULL,
        rating REAL DEFAULT 0.0,
        availability TEXT NOT NULL,
        fetch_at DATE DEFAULT CURRENT_DATE
    )
    ''')

    conn.commit()
    conn.close()

    # Добавляем в список созданных таблиц
    if table_name not in cr:
        cr.append(table_name)

    print(f"✅ Таблица '{table_name}' создана/проверена!")
    return table_name


def add_product(table_name, title, price, rating, availability):
    """Добавляет продукт в указанную таблицу"""
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()

    cursor.execute(f'''
    INSERT INTO {table_name} (title, price, rating, availability)
    VALUES (?, ?, ?, ?)
    ''', (title, price, rating, availability))

    conn.commit()
    conn.close()
    print(f"✅ Продукты добавлены в '{table_name}': {title}")


def show_all_products(table_name):
    """Показывает все продукты из указанной таблицы"""
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        tasks = cursor.fetchall()
    except sqlite3.Error:
        tasks = []  # Если таблицы нет

    conn.close()
    return tasks


def delete_all_products(table_name):
    """Удаляет все продукты из указанной таблицы"""
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name}")
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

    conn.commit()
    conn.close()
    print(f"🗑️ Таблица '{table_name}' очищена")


def get_first_fetch_date(table_name):
    """Получает дату первой записи из таблицы"""
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"SELECT fetch_at FROM {table_name} ORDER BY fetch_at LIMIT 1")
        result = cursor.fetchone()
    except sqlite3.Error:
        result = None

    conn.close()

    if result and result[0]:
        return result[0]  # '2024-01-15'
    return None


def main_base(list_products, cr):
    today = date.today().strftime("%Y%m%d")  # "20240115"
    print(today)
    name = main_category(today, cr=cr)
    product = show_all_products(name)
    if product:
        delete_all_products(name)
        for product in list_products:
            # Извлекаем данные из словаря
            title = product['title']
            price = product['price']
            rating = product['rating']
            availability = product['availability']

            add_product(name, title, price, rating, availability)
    else:
        for product in list_products:
            # Извлекаем данные из словаря
            title = product['title']
            price = product['price']
            rating = product['rating']
            availability = product['availability']
            add_product(name, title, price, rating, availability)
