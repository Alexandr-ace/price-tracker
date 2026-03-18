import requests
from bs4 import BeautifulSoup
import pandas as pd
# Активировать окружение venv\Scripts\activate
# Берем название, цену, наличие, рейтинг с со страниц одного товара


def get_page_preview(url):
    try:
        # Добавляем таймаут, чтобы запрос не "зависал"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Вызовет исключение для 4xx/5xx кодов
        response.encoding = 'utf-8'
        html = response.text
        if not html:
            print("Получена пустая страница.")
            return None
        print("Успех!")
        return html
    except requests.exceptions.Timeout:
        print(f"Таймаут при загрузке {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети для {url}: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def get_page_title(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 1. Находим родительский блок
        price_element = soup.find('div', class_='col-sm-6 product_main')
        if not price_element:
            print("Блок 'product_main' не найден")
            return None
        # 2. Извлекаем заголовок h1 внутри этого блока
        title_element = price_element.find('h1')
        if not title_element:
            print("Заголовок h1 не найден")
            return None
        # 3. Получаем текст заголовка
        title = title_element.text.strip()
        print(title)
        return title  # Лучше возвращать значение, а не только печатать
    except AttributeError as e:
        print(f"Ошибка атрибута: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка в get_page_name: {e}")
        return None


def get_page_price(html):
    try:
        # Необязательно: добавить быструю проверку на пустой html
        if not html or not html.strip():
            print("Получен пустой HTML для анализа.")
            return None
        soup = BeautifulSoup(html, 'html.parser')
        # 1. Сначала находим элемент
        price_element = soup.find('p', class_='price_color')
        if not price_element:
            print("Блок 'price_color' не найден")
            return None
        # 2. Потом извлекаем название
        price_text = price_element.text.strip()  # или .string
        # Необязательно: попробовать преобразовать цену в число (например, '£51.77' -> 51.77)
        # import re
        # clean_price = re.sub(r'[^\d.]', '', price_text)  # Удаляет всё, кроме цифр и точки
        # try:
        #     price_num = float(clean_price)
        # except ValueError:
        #     price_num = None
        # print(f"Цена (текст): {price_text}, Цена (число): {price_num}")
        print(price_text)
        return price_text  # Лучше возвращать значение, а не только печатать
    except AttributeError as e:
        print(f"Ошибка атрибута: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка в get_page_price: {e}")
        return None


def get_page_available(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 1. Сначала находим элемент
        available_element = soup.find('p', class_='instock availability')
        if not available_element:
            print("Блок 'instock availability' не найден")
            return None
        # 2. Получаем текст заголовка
        title = available_element.text.strip()
        # 3. Убираем "In stock (" и последнюю скобку
        # Улучшенная обработка текста:
        result = "Неизвестно"
        if "(" in title and ")" in title:
            # Извлекаем текст в скобках
            result = title.split("(")[-1].split(")")[0]
        else:
            # Если нет скобок, возвращаем весь текст
            result = title
        print(f"Наличие: {result}")
        return result  # Лучше возвращать значение, а не только печатать
    except AttributeError as e:
        print(f"Ошибка атрибута: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка в get_page_available: {e}")
        return None


def get_page_rating(html):
    """
    Извлекает рейтинг книги из HTML.
    Возвращает число от 1 до 5 или 0, если рейтинг не найден.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 1. Сначала находим элемент
        rating_element = soup.find('p', class_='star-rating')

        if not rating_element:
            print("Элемент с рейтингом ('star-rating') не найден на странице.")
            return 0  # Возвращаем 0 вместо None для единообразия

        # Получаем все классы элемента
        classes = rating_element.get('class', [])

        # Ищем класс с рейтингом (One, Two, Three, etc.)
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

        for cls in classes:
            if cls in rating_map:
                rating = rating_map[cls]
                print(f"Рейтинг: {rating}/5")
                return rating

        # Если дошли сюда, значит класс рейтинга не найден
        print("Класс рейтинга (One, Two, Three...) не обнаружен в элементе.")
        return 0

    except AttributeError as e:
        print(f"Ошибка при обращении к атрибуту элемента рейтинга: {e}")
        return 0
    except Exception as e:
        print(f"Не удалось извлечь рейтинг: {e}")
        return 0


def parse_single_product(html):
    """Парсит все данные со страницы одного товара"""
    if not html:
        print("Не получен HTML для парсинга.")
        return None

    product_data = {
        'title': get_page_title(html),
        'price': get_page_price(html),
        'availability': get_page_available(html),
        'rating': get_page_rating(html)  # Теперь это число 0-5
    }

    # Проверяем, что хотя бы некоторые данные получены
    if all(value is None for value in product_data.values()):
        print("Не удалось извлечь никаких данных о товаре.")
        return None

    return product_data

# Берем название, цену, наличие, рейтинг со страницы на которой несколько товаров


def get_page_all(html):
    # Сохранение данных в список словарей:
    books_data = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        product_articles = soup.find_all('article', class_='product_pod')

        if not product_articles:
            print("Элементы не найдены!")
            return books_data  # Возвращаем пустой список

        print(f"Найдено {len(product_articles)} товаров")

        for article in product_articles:
            try:
                book_info = {}

                # Название (с проверкой)
                title_elem = article.find('h3')
                if title_elem:
                    title_link = title_elem.find('a')
                    book_info['title'] = title_link.text.strip(
                    ) if title_link else "Без названия (нет ссылки)"
                else:
                    book_info['title'] = "Без названия"

                # Цена (с проверкой)
                price_elem = article.find('p', class_='price_color')
                book_info['price'] = price_elem.text.strip(
                ) if price_elem else "N/A"

                # Рейтинг (обратите внимание, что класс для наличия может отличаться)
                rating_elem = article.find('p', class_='star-rating')
                book_info['rating'] = 0
                if rating_elem:
                    classes = rating_elem.get('class', [])
                    rating_map = {'One': 1, 'Two': 2,
                                  'Three': 3, 'Four': 4, 'Five': 5}
                    for cls in classes:
                        if cls in rating_map:
                            book_info['rating'] = rating_map[cls]
                            break

                availability_elem = article.find(
                    'p', class_='instock availability')  # или 'availability'
                book_info['availability'] = availability_elem.text.strip(
                ) if availability_elem else "Неизвестно"
                # Добавляем в список
                books_data.append(book_info)

            except Exception as e:
                print(f"Ошибка при обработке карточки товара: {e}")
                continue  # Продолжаем обработку остальных товаров

    except Exception as e:
        print(f"Критическая ошибка в get_page_all: {e}")
    # Теперь у вас есть список всех книг
    print(f"Собрано данных о {len(books_data)} книгах")
    return books_data


# Сохраняем в CSV файл
def file_csv_funk(csv_file):
    if not csv_file:
        print("Нет данных для сохранения.")
        return
    # Создаем DataFrame
    try:
        df = pd.DataFrame(csv_file)

        # Сохраняем в CSV
        df.to_csv('books_data.csv', index=False, encoding='utf-8-sig')
        print("Данные сохранены в books_data.csv")

        # Сохраняем в Excel (если нужно)
        try:
            df.to_excel('books_data.xlsx', index=False)
            print("Данные также сохранены в books_data.xlsx")
        except Exception as e:
            print(f"Не удалось сохранить в Excel: {e}")

        print("Первые строки данных:")
        print(df.head())
    except PermissionError:
        print("Ошибка: Нет прав на запись файла или файл открыт в другой программе.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


# Основной блок
if __name__ == "__main__":
    # Получаем HTML для одиночной страницы
    arg = get_page_preview(
        "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html")

    if arg:
        data = parse_single_product(arg)
        if data:
            print(f"Спарсены данные: {data}")
    else:
        print("Не удалось загрузить страницу товара.")

    # Получаем HTML для страницы каталога
    arg_page = get_page_preview(
        "https://books.toscrape.com/catalogue/page-1.html")

    if arg_page:
        csv_file = get_page_all(arg_page)
        if csv_file:  # Проверяем, что есть что сохранять
            file_csv_funk(csv_file)
        else:
            print("Нет данных для создания CSV.")
    else:
        print("Не удалось загрузить страницу каталога.")
