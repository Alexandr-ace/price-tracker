import requests
from bs4 import BeautifulSoup


def get_page_preview(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        html = response.text
        print(f"Успех! Получено {len(html)} символов")
    else:
        print("Сайт не отвечает :(")
        pass
    soup = BeautifulSoup(html, 'html.parser')
    # 1. Сначала находим элемент
    price_element = soup.find('p', class_='price_color')
    # 2. Потом извлекаем текст
    price_text = price_element.text  # или .string
    print(price_text)


# Тест
get_page_preview(
    "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html")
# print(preview)
