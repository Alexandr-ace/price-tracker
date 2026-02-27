import sqlite3
from datetime import date
import re


def get_last_fetch_date(table_name):
    """Получает дату последней записи из таблицы в формате YYYYMMDD"""
    conn = sqlite3.connect('parce_base_single.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"SELECT fetch_at FROM {table_name} ORDER BY fetch_at DESC LIMIT 1")
        result = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Ошибка при получении даты из таблицы '{table_name}': {e}")
        result = None

    conn.close()

    if result and result[0]:
        date_str = str(result[0]).replace('-', '')
        return date_str
    return None


def delete_last_record_by_date(table_name):
    """Удаляет запись с самой последней датой из таблицы и обновляет автоинкремент"""
    conn = sqlite3.connect('parce_base_single.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT id, fetch_at FROM {table_name} 
            ORDER BY fetch_at DESC, id DESC 
            LIMIT 1
        """)
        last_record = cursor.fetchone()

        if last_record:
            last_id = last_record[0]
            cursor.execute(
                f"DELETE FROM {table_name} WHERE id = ?", (last_id,))

            # Проверяем, остались ли записи в таблице
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            remaining_count = cursor.fetchone()[0]

            if remaining_count == 0:
                # Если таблица пустая - сбрасываем автоинкремент
                cursor.execute(
                    f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
                print(
                    f"🔄 Автоинкремент сброшен для пустой таблицы '{table_name}'")
            else:
                # Если есть другие записи - находим максимальный ID
                cursor.execute(f"SELECT MAX(id) FROM {table_name}")
                max_id = cursor.fetchone()[0]
                # Обновляем последовательность на текущий максимальный ID
                cursor.execute(
                    f"UPDATE sqlite_sequence SET seq={max_id} WHERE name='{table_name}'")
                print(
                    f"🔄 Автоинкремент обновлен до {max_id} для таблицы '{table_name}'")

            conn.commit()
            print(
                f"🗑️ Удалена запись (ID: {last_id}) из таблицы '{table_name}'")
        else:
            print(f"⚠️  В таблице '{table_name}' нет записей для удаления")

    except sqlite3.Error as e:
        print(f"❌ Ошибка при удалении записи из таблицы '{table_name}': {e}")
    finally:
        conn.close()


def sanitize_table_name(name):
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


def main_category_single(table_suffix):
    """Создает таблицу tasks с указанным суффиксом"""
    safe_suffix = sanitize_table_name(table_suffix)
    table_name = f"tasks_{safe_suffix}"

    conn = sqlite3.connect('parce_base_single.db')
    cursor = conn.cursor()

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price_with_card TEXT NOT NULL,
        price_without_card TEXT NOT NULL,
        rating REAL DEFAULT 0.0,
        availability TEXT NOT NULL,
        fetch_at DATE DEFAULT CURRENT_DATE
    )
    ''')

    conn.commit()
    conn.close()

    print(f"✅ Таблица '{table_name}' создана/проверена!")
    return table_name


def add_product_single(table_name, title, price_with_card, price_without_card, rating, availability):
    """Добавляет продукт в указанную таблицу"""
    conn = sqlite3.connect('parce_base_single.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
        INSERT INTO {table_name} (title, price_with_card, price_without_card, rating, availability)
        VALUES (?, ?, ?, ?, ?)
        ''', (title, price_with_card, price_without_card, rating, availability))
        conn.commit()
        print(f"✅ Продукт добавлен в '{table_name}': {title[:30]}...")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при добавлении продукта: {e}")
    finally:
        conn.close()


def show_all_products_single(table_name):
    """Показывает все продукты из указанной таблицы"""
    conn = sqlite3.connect('parce_base_single.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        tasks = cursor.fetchall()
    except sqlite3.Error:
        tasks = []  # Если таблицы нет

    conn.close()
    return tasks

# Для списка одного товара


def init_meta_table():
    conn = sqlite3.connect('parce_base_single.db')
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


def add_to_meta_table(title):
    """Добавляет продукт в указанную таблицу"""
    conn = sqlite3.connect('parce_base_single.db')
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


def is_table_in_meta(original_title):
    """Проверяет, есть ли товар в мета-таблице"""
    conn = sqlite3.connect('parce_base_single.db')
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT title FROM data_center WHERE title = ?",
        (original_title,)
    )

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None
