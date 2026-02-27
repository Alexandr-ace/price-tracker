from bs4 import BeautifulSoup
import pandas as pd
# Импорт всех необходимых компонентов
from selenium import webdriver  # Главный класс для управления браузером
# Класс с константами для поиска (By.ID, By.CSS_SELECTOR)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Класс для явного ожидания
from selenium.webdriver.support import expected_conditions as EC  # Условия для ожидания
# Класс для настройки опций Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time  # Для принудительных пауз (использовать с осторожностью)
from selenium.common.exceptions import TimeoutException, WebDriverException
import re
# Активировать окружение venv\Scripts\activate
# Берем название, цену, наличие, рейтинг с со страниц одного товара


def get_page_preview(url, page_type='product'):
    # Инициализируем driver как None, чтобы обработать случай, если ошибка произойдёт до его создания
    driver = None
    try:
        chrome_options = Options()
        user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent_string}")
        # Частично скрывает автоматизацию
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        # Убирает всплывающее уведомление "Chrome управляется..."
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        # Переходим на страницу товара Ozon
        # Замените на реальный URL
        driver.get(url)
        # Создаем объект для ЯВНОГО ожидания (более гибкого, чем неявное).
        # Он будет использоваться для конкретных условий.
        # Максимальное время ожидания - 15 секунд
        wait = WebDriverWait(driver, 15)
        if page_type == 'product':
            # Ожидание для страницы товара
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "[data-widget='webProductHeading'] h1"))
            )
        else:
            # 1. Ждём появления первых карточек
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.tile-root"))
            )
            # 2. Умное ожидание: ждём 20 товаров, но не больше 7 секунд
            print("Ожидаю загрузки товаров...")
            try:
                WebDriverWait(driver, 7).until(
                    lambda d: len(d.find_elements(
                        By.CSS_SELECTOR, "div.tile-root")) >= 20
                )
                print(
                    f"Загружено товаров: {len(driver.find_elements(By.CSS_SELECTOR, 'div.tile-root'))}")
            except TimeoutException:
                # Если за 7 секунд не набралось 20 товаров - берём то, что есть
                current_count = len(driver.find_elements(
                    By.CSS_SELECTOR, "div.tile-root"))
        # Как только элемент стал видимым, извлекаем из него текст или вытаскиваем всё что нам нужно из стрницы в целом
        # product_title = title_element.text
        # print(f"Название товара: {product_title}")
        html = driver.page_source
        return html
    except TimeoutException:
        print(f"Таймаут при загрузке элемента на {url}")
        return None
    except WebDriverException as e:
        print(f"Ошибка WebDriver для {url}: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке {url}: {e}")
        return None
    finally:
        # Этот блок выполнится ВСЕГДА: и при успехе, и при любой ошибке
        if driver is not None:  # Проверяем, был ли создан driver
            driver.quit()
            print("Драйвер закрыт в блоке finally")


def get_page_title(html):
    """
    Извлекает название товара из HTML страницы Ozon.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 1. Находим виджет-контейнер с заголовком товара
        # На Ozon заголовок находится внутри виджета с data-widget='webProductHeading'
        title_widget = soup.find('div', {'data-widget': 'webProductHeading'})

        if not title_widget:
            print("Виджет 'webProductHeading' не найден")
            return None
        # 2. Извлекаем заголовок h1 внутри этого виджета
        # На Ozon h1 может быть не прямым потомком, используем find() для поиска в глубину
        title_element = title_widget.find('h1')
        if not title_element:
            # Альтернативный поиск: попробуем найти любой заголовочный элемент
            title_element = title_widget.find(['h1', 'h2', 'h3'])
        if not title_element:
            print("Заголовок не найден внутри виджета")
            return None
        # 3. Получаем текст заголовка
        title = title_element.text.strip()
        print(f"Название товара: {title}")
        return title
    except AttributeError as e:
        print(f"Ошибка атрибута при парсинге: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка в get_ozon_product_title: {e}")
        return None


def get_page_price(html):
    """
    Извлекает цены товара из HTML страницы Ozon.
    Работает на основе постоянных классов: tsHeadline600Large и tsHeadline500Medium
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # 1. Находим виджет цены (основной контейнер)
        price_widget = soup.find('div', {'data-widget': 'webPrice'})

        if not price_widget:
            print("Виджет 'webPrice' не найден")
            return None

        prices = {'with_card': None, 'without_card': None}

        # 2. Ищем цену с Ozon Картой (tsHeadline600Large)
        # Ищем ВНУТРИ виджета webPrice
        card_price_elem = price_widget.find(
            'span', class_='tsHeadline600Large')
        if card_price_elem:
            prices['with_card'] = card_price_elem.text.strip()

        # 3. Ищем цену без Ozon Карты (tsHeadline500Medium)
        # Ищем ВНУТРИ виджета webPrice
        without_card_price_elem = price_widget.find(
            'span', class_='tsHeadline500Medium')
        if without_card_price_elem:
            prices['without_card'] = without_card_price_elem.text.strip()

        # 4. Очищаем от специальных символов
        for key in prices:
            if prices[key]:
                prices[key] = prices[key].replace('\u2009', ' ').replace(
                    '\u202f', ' ').replace('\xa0', ' ')

        print(f"Найденные цены: {prices}")

        # 5. Проверяем, нашли ли хотя бы одну цену
        if not any(prices.values()):
            print("Не удалось найти цены в виджете")
            return None

        return prices

    except Exception as e:
        print(f"Ошибка при парсинге цен: {e}")
        return None


def get_page_not_available_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_widget = soup.find('div', {'data-widget': 'webSale'})
    if not price_widget:
        print("Виджет цены не найден")
        return None
    prices = {'price': None, 'available': None}
    card_label = price_widget.find(
        'span', class_='tsHeadline600Large')
    if card_label:
        prices['price'] = card_label.text.strip().replace(
            '\u2009', ' ').replace('\u202f', ' ').replace('\xa0', ' ')
        return prices


def get_page_available(html):
    """
    Супер-простая проверка: ищем только виджет webAddToCart
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        price_widget = soup.find('div', {'data-widget': 'webSale'})
        if not price_widget:
            print("Виджет цены не найден")
            return None
        card_price_elem = price_widget.find(
            'span', class_='tsBodyControl500Medium')
        # Если есть виджет добавления в корзину - товар в наличии
        if card_price_elem and any(phrase in card_price_elem.text for phrase in ['Узнать о поступлении', 'Нет в наличии']):
            return 'out_of_stock'
        else:
            return 'in_stock'

    except Exception as e:
        print(f"Ошибка при проверке наличия товара: {e}")
        return None


def get_page_rating(html):
    """
    Извлекает рейтинг книги из HTML.
    Возвращает число от 1 до 5 или 0, если рейтинг не найден.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 1. Сначала находим элемент
        rating_widget = soup.find(
            'div', {'data-widget': 'webSingleProductScore'})
        if not rating_widget:
            print("Элемент с рейтингом не найден на странице.")
            return 0.0  # Возвращаем 0 вместо None для единообразия
        card_rating_elem = rating_widget.find(
            'div', class_='tsBodyControl500Medium')
        if card_rating_elem:
            # 1. Получаем сырой текст
            raw_text = card_rating_elem.text.strip()
            print(f"[DEBUG] Сырой текст рейтинга: '{raw_text}'")
            # 2. Ищем в строке первое число (целое или с точкой)
            # Шаблон для чисел вида 4, 4.6, 4.67
            match = re.search(r'[\d]+\.?[\d]*', raw_text)
            if match:
                # 3. Если нашли число - преобразуем его в float и возвращаем
                rating = float(match.group(0))
                print(f"[УСПЕХ] Извлечен чистый рейтинг: {rating}")
                return rating
            else:
                # 4. Если не нашли число - возвращаем 0
                print("[ОШИБКА] В тексте не найдено числового рейтинга.")
                return 0.0
        else:
            rating = 0.0
            print(rating)
            return rating
    except AttributeError as e:
        print(f"Ошибка при обращении к атрибуту элемента рейтинга: {e}")
        return 0.0
    except Exception as e:
        print(f"Не удалось извлечь рейтинг: {e}")
        return 0.0


def parse_single_product(html):
    """Парсит все данные со страницы одного товара Ozon"""
    if not html:
        print("Не получен HTML для парсинга.")
        return None

    product_data = {
        'title': get_page_title(html),
        'availability': get_page_available(html),
        'rating': get_page_rating(html),
    }

    # Получаем цены в зависимости от наличия
    availability = product_data['availability']
    if availability == 'in_stock':
        prices = get_page_price(html)
        if prices:
            product_data['price_with_card'] = prices.get('with_card')
            product_data['price_without_card'] = prices.get('without_card')
    elif availability == 'out_of_stock':
        price_data = get_page_not_available_price(html)
        if price_data:
            product_data['out_of_stock_price'] = price_data.get('price')

    # Проверяем, что хотя бы некоторые данные получены
    if all(value is None for value in product_data.values()):
        print("Не удалось извлечь никаких данных о товаре.")
        return None

    return product_data


def file_csv_funk(csv_file, filename_prefix='ozon'):
    """Сохраняет данные в CSV и Excel файлы"""
    if not csv_file:
        print("Нет данных для сохранения.")
        return

    try:
        df = pd.DataFrame(csv_file)

        # Сохраняем в CSV
        csv_filename = f'{filename_prefix}_data.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"Данные сохранены в {csv_filename}")

        # Сохраняем в Excel
        try:
            excel_filename = f'{filename_prefix}_data.xlsx'
            df.to_excel(excel_filename, index=False)
            print(f"Данные также сохранены в {excel_filename}")
        except Exception as e:
            print(f"Не удалось сохранить в Excel: {e}")

        print("\nПервые строки данных:")
        print(df.head())

        return df

    except PermissionError:
        print("Ошибка: Нет прав на запись файла или файл открыт в другой программе.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

    return None


def get_page_all(html):
    # Сохранение данных в список словарей:
    books_data = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        product_articles = soup.find_all('div', class_='tile-root')

        if not product_articles:
            print("Элементы не найдены!")
            return books_data  # Возвращаем пустой список

        print(f"Найдено {len(product_articles)} товаров")

        for index, article in enumerate(product_articles):
            try:
                book_info = {}

                # Название (с проверкой)
                title_elem = article.find('span', class_='tsBody500Medium')
                if title_elem:
                    book_info['title'] = title_elem.text.strip(
                    ) if title_elem else "Без названия (нет ссылки)"
                else:
                    book_info['title'] = "Без названия"

                # Цена (с проверкой)
                price_elem = article.find('span', class_='tsHeadline500Medium')
                book_info['price'] = price_elem.text.strip(
                ) if price_elem else "N/A"

                # Рейтинг (обратите внимание, что класс для наличия может отличаться)
                rating_elem = article.find(
                    'div', class_='tsBodyMBold')
                if rating_elem:
                    # Находим ВСЕ span внутри div
                    all_spans = rating_elem.find_all('span')
                    for span in all_spans:
                        match = re.search(
                            r'[\d]+[.,]?[\d]*', span.text.strip())
                        if match:
                            book_info['rating'] = float(
                                match.group().replace(',', '.'))
                            break  # Нашли первый подходящий span - выходим
                else:
                    print("рейтинг не найден")
                    book_info['rating'] = 0.0

                # Наличие
                availability_elem = article.find(
                    'div', class_='tsBodyControl500Medium')  # или 'availability'
                book_info['availability'] = 'out_of_stock' if availability_elem else 'in_stock'
                # Добавляем в список
                books_data.append(book_info)
                if index > 0 and (index + 1) % 5 == 0:
                    print(f"  Обработано {index + 1} товаров. Делаю паузу...")
                    time.sleep(2)  # Пауза 2 секунды

            except Exception as e:
                print(f"Ошибка при обработке карточки товара: {e}")
                continue  # Продолжаем обработку остальных товаров

    except Exception as e:
        print(f"Критическая ошибка в get_page_all: {e}")
    # Теперь у вас есть список всех книг
    print(f"Собрано данных о {len(books_data)} товарах")
    return books_data


# Тестируем
# Основной блок
if __name__ == "__main__":
    # === ТЕСТ ОДНОГО ТОВАРА ===
    print("=== Тест одного товара ===")
    single_product_url = "https://www.ozon.ru/product/pogranichnaya-trilogiya-makkarti-kormak-600817501/?at=Eqtkx1WmJhxlQKPqSk0vp1Wuk1VkyQfkrnpMgSW02PZJ"

    single_html = get_page_preview(single_product_url, page_type='product')
    if single_html:
        product_data = parse_single_product(single_html)
        if product_data:
            print(f"\nДанные товара:")
            for key, value in product_data.items():
                print(f"  {key}: {value}")
    else:
        print("Не удалось загрузить страницу товара.")

    # === ПАРСИНГ СПИСКА ТОВАРОВ ===
    print("\n=== Парсинг списка товаров ===")
    category_url = "https://www.ozon.ru/category/shapki-zhenskie-36513/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=шапка+зимняя+женская"

    list_html = get_page_preview(category_url, page_type='category')
    if list_html:
        all_products = get_page_all(list_html)
        if all_products:
            # Сохраняем в файл
            df = file_csv_funk(all_products, filename_prefix='ozon_products')
        else:
            print("Нет данных для создания CSV.")
    else:
        print("Не удалось загрузить страницу категории.")

    print("\n=== ВЫПОЛНЕНИЕ ЗАВЕРШЕНО ===")
