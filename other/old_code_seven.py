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
# Активировать окружение venv\Scripts\activate
# Берем название, цену, наличие, рейтинг с со страниц одного товара


def get_page_preview(url):
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
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-widget='webProductHeading'] h1"))
        )
        # Как только элемент стал видимым, извлекаем из него текст или вытаскиваем всё что нам нужно из стрницы в целом
        # product_title = title_element.text
        # print(f"Название товара: {product_title}")
        html = driver.page_source
        return html  # Возвращаем html здесь, до блока finally
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
        if card_price_elem:
            print(
                f"[DEBUG] Найден элемент отсутствия: {card_price_elem.text[:50]}...")
            return 'out_of_stock'
        else:
            print("[DEBUG] Элемент отсутствия не найден. Товар в наличии.")
            return 'in_stock'

    except Exception as e:
        print(f"Ошибка при проверке наличия товара: {e}")
        return None


# Тестируем
arg = get_page_preview(
    "https://www.ozon.ru/product/eres-horusa-t-6-epoha-tmy-otverzhennye-mertvetsy-poteryannoe-osvobozhdenie-rasskazy-romany-1418521987/?oos_search=false")

get_page_title(arg)

if arg:
    availability = get_page_available(arg)
    print(f"Наличие: {availability}")
    if availability == 'in_stock':
        prices = get_page_price(arg)
        print(f"Цены: {prices}")
    elif availability == 'out_of_stock':
        price = get_page_not_available_price(arg)
        print(f"Цена: {price}")
