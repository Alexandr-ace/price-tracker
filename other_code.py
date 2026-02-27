today = date.today().strftime("%Y%m%d")  # "20240115"
print(today)
name = main_category(today)
product = show_all_products(name)
if product:
    date_create = get_first_fetch_date(name)
    if date_create:
        date_create_formatted = date_create.replace("-", "")
        print(f"📅 Дата первой записи в таблице: {date_create}")
        print(f"📅 Дата после преобразования: {date_create_formatted}")

        if date_create_formatted == today:
            print("🔄 Таблица сегодняшняя, перезаписываем...")
            delete_all_products(name)
            add_product(name, title, price, rating, availability)
        else:
            print("Ошибка")
    else:
        print("❌ Не удалось получить дату из таблицы")
        # На всякий случай очищаем и добавляем
        delete_all_products(name)
        add_product(name, title, price, rating, availability)
else:
    add_product(name, title, price, rating, availability)
