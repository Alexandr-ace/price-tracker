import sqlite3
from datetime import date
import re
# Если таблица сегодня существует, значит мы ее полностью перезаписываем
# Но если стоит другое число, значит создаём новую, а струю сохраняем
# Тестируем


def main_category(table_suffix, table_prefix):
    """Создает таблицу tasks с указанным суффиксом"""
    table_name = f"tasks_{table_prefix}_{table_suffix}"

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
        cursor.execute(f"SELECT fetch_at FROM {table_name} LIMIT 1")
        result = cursor.fetchone()
    except sqlite3.Error:
        result = None

    conn.close()
    return result[0] if result else None


# Для списка товаров
def init_meta_table_many():
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS data_center (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        fetch_at DATE DEFAULT CURRENT_DATE
    )
    ''')

    conn.commit()
    conn.close()


def add_to_meta_table_many(title):
    """Добавляет продукт в указанную таблицу"""
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO data_center (title)
        VALUES (?)
        ''', (title,))
        conn.commit()
        print(f"✅ Товар '{title[:30]}...' добавлен в мета-таблицу")
    except sqlite3.IntegrityError:
        # Уже существует
        pass
    except Exception as e:
        print(f"❌ Ошибка при добавлении в мета-таблицу: {e}")
    finally:
        conn.close()


def is_table_in_meta_many(original_title):
    """Проверяет, есть ли товар в мета-таблице"""
    conn = sqlite3.connect('parce_base.db')
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT title FROM data_center WHERE title = ?",
        (original_title,)
    )

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def sanitize_table_name_many(name):
    """Преобразует название товара в безопасное имя для таблицы SQL"""
    if not name:
        return 'unknown_product'

    safe_name = re.sub(r'[^\w\s-]', '', name)
    safe_name = re.sub(r'[\s-]+', '_', safe_name)
    safe_name = safe_name.strip('_')
    safe_name = safe_name[:50]

    if not safe_name:
        safe_name = 'product'

    return safe_name.lower()
