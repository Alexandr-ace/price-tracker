import requests
from bs4 import BeautifulSoup

# Берем название, цену, наличие, рейтинг с со страниц одного товара


def get_page_preview(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        html = response.text
        print("Успех!")
        return html
    else:
        print("Сайт не отвечает :(")


def get_page_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 1. Находим родительский блок
    price_element = soup.find('div', class_='col-sm-6 product_main')
    # 2. Извлекаем заголовок h1 внутри этого блока
    title_element = price_element.find('h1')
    # 3. Получаем текст заголовка
    title = title_element.text.strip()
    print(title)


def get_page_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 1. Сначала находим элемент
    price_element = soup.find('p', class_='price_color')
    # 2. Потом извлекаем название
    price_text = price_element.text.strip()  # или .string
    print(price_text)


def get_page_available(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 1. Сначала находим элемент
    available_element = soup.find('p', class_='instock availability')
    # 2. Получаем текст заголовка
    title = available_element.text.strip()
    # 3. Убираем "In stock (" и последнюю скобку
    result = title.split("(")[-1].rstrip(")")
    print(result)  # "20 available"


def get_page_rating(html):
    soup = BeautifulSoup(html, 'html.parser')
    rating_element = soup.find('p', class_='star-rating')
    if rating_element:
        # 1. Смотрим все классы родительского элемента
        classes = rating_element.get('class', [])
        # 2. Ищем класс с рейтингом (One, Two, Three, etc.)
        rating_classes = [c for c in classes if c in [
            'One', 'Two', 'Three', 'Four', 'Five']]
        if rating_classes:
            rating_word = rating_classes[0]
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_map.get(rating_word, 0)
            print(f"Рейтинг:{rating}/5")


# Берем название, цену, наличие, рейтинг с со страницы на которой несколько товаров

def get_page_all(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_articles = soup.find_all('article', class_='product_pod')
    if not product_articles:
        print("Элементы не найдены!")
    else:
        print(f"Найдено {len(product_articles)} товаров")
    # Сохранение данных в список словарей:
    books_data = []
    for article in product_articles:
        book_info = {}
        # Название
        title_elem = article.find('h3').find('a')
        book_info['title'] = title_elem.text.strip(
        ) if title_elem else "Без названия"

        # Цена
        price_elem = article.find('p', class_='price_color')
        book_info['price'] = price_elem.text.strip() if price_elem else "N/A"

        # Рейтинг
        rating_elem = article.find('p', class_='star-rating')
        if rating_elem:
            classes = rating_elem.get('class', [])
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            for cls in classes:
                if cls in rating_map:
                    book_info['rating'] = rating_map[cls]
                    break
        else:
            book_info['rating'] = 0

        # Наличие
        avalible_elem = article.find('p', class_='availability')
        book_info['avalible'] = avalible_elem.text.strip()

        # Добавляем в список
        books_data.append(book_info)
    # Теперь у вас есть список всех книг
    print(f"Собрано данных о {len(books_data)} книгах")


arg = get_page_preview(
    "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html")
arg_page = get_page_preview(
    "https://books.toscrape.com/catalogue/page-1.html")

get_page_name(arg)
get_page_price(arg)
get_page_available(arg)
get_page_rating(arg)
get_page_all(arg_page)
