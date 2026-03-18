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

# --- ШАГ 1: КОНФИГУРАЦИЯ БРАУЗЕРА (ДО его запуска) ---
chrome_options = Options()  # Создаем объект для хранения настроек
# ОПЦИЯ 1: Режим "без головы" (без графического интерфейса). Раскомментируйте для работы в фоне.
# chrome_options.add_argument("--headless=new")

# ОПЦИЯ 2: Устанавливаем User-Agent вручную. Можно скопировать строку из своего браузера.
user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent_string}")

# ОПЦИЯ 3: Другие полезные аргументы для маскировки под обычный браузер
# Частично скрывает автоматизацию
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# Убирает всплывающее уведомление "Chrome управляется..."
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])


# --- ШАГ 2: ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА (Запуск браузера) ---
# Автоматическая настройка драйвера
# Service теперь ОБЯЗАТЕЛЕН для новых версий Selenium (4.6.0+)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
# Устанавливаем НЕЯВНОЕ ожидание. Это ГЛОБАЛЬНАЯ настройка для ВСЕХ операций поиска элементов.
# Драйвер будет ждать до 10 секунд, пока элемент не появится в DOM, прежде чем выбросить ошибку.
driver.implicitly_wait(10)

# --- ШАГ 3: ОТКРЫТИЕ СТРАНИЦЫ И РАБОТА С ЯВНЫМИ ОЖИДАНИЯМИ ---
try:
    # 3.1. Переходим на страницу товара Ozon
    # Замените на реальный URL
    product_url = "https://www.ozon.ru/product/example-product-id/"
    driver.get(product_url)
    print("Страница загружается...")

    # 3.2. Создаем объект для ЯВНОГО ожидания (более гибкого, чем неявное).
    # Он будет использоваться для конкретных условий.
    wait = WebDriverWait(driver, 15)  # Максимальное время ожидания - 15 секунд

    # --- ПРИМЕР 1: Ожидание загрузки основного названия товара ---
    # Мы ждем не просто появления тега <h1> в коде (presence),
    # а того момента, когда он станет ВИДИМЫМ (visibility) на экране пользователя.
    # Это надежнее, так как элемент может быть скрыт CSS.
    title_element = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "h1[data-widget='webProductHeading']"))
    )
    # Как только элемент стал видимым, извлекаем из него текст.
    product_title = title_element.text
    print(f"Название товара: {product_title}")

    # --- ПРИМЕР 2: Ожидание и клик по кнопке (например, "Показать все характеристики") ---
    # Часто на Ozon детали скрыты под кнопками, которые подгружают контент через JS.
    # Мы ждем, пока кнопка не станет КЛИКАБЕЛЬНОЙ (видимой и активной).
    try:
        show_specs_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button//span[contains(text(), 'Все характеристики')]/ancestor-or-self::button"))
        )
        show_specs_button.click()
        print("Кликнули на кнопку 'Все характеристики'. Ждем загрузки...")
        # Иногда после клика нужно дать время на подгрузку контента. WebDriverWait здесь может быть сложнее применить.
        time.sleep(1.5)
    except Exception as e:
        print(
            f"Кнопка 'Все характеристики' не найдена или не кликабельна: {e}")

    # --- ПРИМЕР 3: Скроллинг для подгрузки динамического контента (отзывов) ---
    # Selenium может кликать только по видимым элементам.
    # Чтобы подгрузить отзывы, которые загружаются при прокрутке, имитируем скролл.
    print("Скроллим страницу для подгрузки отзывов...")
    old_height = driver.execute_script("return document.body.scrollHeight")
    # Скролл в самый низ
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Ждем, пока JavaScript сайта успеет подгрузить новый контент
    time.sleep(2.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(f"Высота страницы до скролла: {old_height}, после: {new_height}")

    # --- ПРИМЕР 4: Сбор данных из подгруженного контента ---
    # После скролла пробуем найти блоки с отзывами.
    # find_elements возвращает СПИСОК всех найденных элементов. Если список пуст — отзывов нет.
    review_blocks = driver.find_elements(
        By.CSS_SELECTOR, "[data-widget='webReviewProduct'] .review")
    print(f"Найдено блоков с отзывами на странице: {len(review_blocks)}")

    # Проходим по первым 3 отзывам и выводим текст.
    for i, review in enumerate(review_blocks[:3]):
        try:
            # Внутри каждого блока ищем текстовый элемент. Поиск ведется ОТ ЭТОГО БЛОКА (review.find_element).
            review_text_elem = review.find_element(
                By.CSS_SELECTOR, ".review-text")
            # Выводим первые 100 символов
            print(f"Отзыв #{i+1}: {review_text_elem.text[:100]}...")
        except:
            print(f"Не удалось извлечь текст из отзыва #{i+1}")

    # --- ШАГ 4: СОХРАНЕНИЕ ИСХОДНОГО КОДА СТРАНИЦЫ ---
    # После всех манипуляций и подгрузок можно получить финальный HTML и отдать его BeautifulSoup.
    final_page_html = driver.page_source
    # Теперь с `final_page_html` можно работать как с обычным HTML в BeautifulSoup.
    print("Исходный код страницы готов для анализа BeautifulSoup.")

except Exception as e:
    # Обработка любых ошибок, возникших в основном блоке кода.
    print(f"В процессе работы произошла ошибка: {type(e).__name__}: {e}")

finally:
    # --- ШАГ 5: КОРРЕКТНОЕ ЗАВЕРШЕНИЕ РАБОТЫ ---
    # Блок `finally` выполнится ВСЕГДА, даже если выше была ошибка.
    # Пауза, чтобы вы могли оценить результат
    input("Нажмите Enter в этом окне консоли, чтобы закрыть браузер...")
    # Закрывает все окна браузера и завершает процесс драйвера. ОБЯЗАТЕЛЬНО.
    driver.quit()
    print("Браузер закрыт, ресурсы освобождены.")
