import sqlite3


def add_task(title, description="", priority=1):
    """Добавляет новую задачу в базу данных"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    # Вставляем данные (вопросительные знаки защищают от SQL-инъекций)
    cursor.execute('''
    INSERT INTO tasks (title, description, priority)
    VALUES (?, ?, ?)
    ''', (title, description, priority))

    conn.commit()
    conn.close()
    print(f"✅ Задача добавлена: {title}")


def show_all_tasks():
    """Показывает все задачи"""
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    # Получаем ВСЕ записи из таблицы tasks
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("📭 Список задач пуст")
        return

    print("\n📋 ВСЕ ЗАДАЧИ:")
    print("-" * 50)

    for task in tasks:
        task_id, title, desc, priority, status, created, completed = task

        priority_text = {1: "📌 Низкий", 2: "⚠️ Средний",
                         3: "🔥 Высокий"}.get(priority, "?")
        status_text = {"todo": "🟡 К выполнению", "in_progress": "🟠 В работе",
                       "done": "✅ Выполнено"}.get(status, "?")

        print(f"ID: {task_id}")
        print(f"Задача: {title}")
        print(f"Описание: {desc}")
        print(f"Приоритет:{priority_text}")
        print(f"Статус: {status_text}")
        print(f"Создана: {created}")
        if completed:
            print(f"Завершена: {completed}")
        print("-" * 30)


def update_task_status(task_id, new_status):
    """Изменяет статус задачи"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    if new_status == 'done':
        # Если задача завершена, ставим дату завершения
        cursor.execute('''
        UPDATE tasks 
        SET status = ?, completed_at = CURRENT_TIMESTAMP 
        WHERE id = ?
        ''', (new_status, task_id))
    else:
        cursor.execute('''
        UPDATE tasks 
        SET status = ?, completed_at = NULL 
        WHERE id = ?
        ''', (new_status, task_id))

    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        print(f"✅ Статус задачи {task_id} изменен на '{new_status}'")
    else:
        print(f"❌ Задача с ID {task_id} не найдена")


def update_task_status(new_status, task_id):
    """Изменяет статус задачи"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    if new_status == "done":
        # Если задача завершена, ставим дату завершения
        cursor.execute('''
        UPDATE tasks
        SET status = ?, completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (new_status, task_id))
    else:
        cursor.execute('''
        UPDATE tasks
        SET status = ?, completed_at = NULL
        WHERE id = ?
        ''', (new_status, task_id))

    conn.commit()
    conn.close()
    # cursor.rowcount - количество затронутых строк последней операцией
    if cursor.rowcount > 0:
        print(f"✅ Статус задачи {task_id} изменен на '{new_status}'")
    else:
        print(f"❌ Задача с ID {task_id} не найдена")


def delete_task(task_id):
    """Удаляет задачу по ID"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        print(f"✅ Задача {task_id} удалена")
    else:
        print(f"❌ Задача с ID {task_id} не найдена")


def search_tasks(keyword):
    """Ищет задачи по ключевому слову"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    # Ищем в названии и описании
    cursor.execute('''
    SELECT * FROM tasks 
    WHERE title LIKE ? OR description LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))

    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print(f"🔍 Задачи по запросу '{keyword}' не найдены")
        return

    print(f"\n🔍 РЕЗУЛЬТАТЫ ПОИСКА ('{keyword}'):")
    for task in tasks:
        print(f"[{task[0]}] {task[1]} - {task[4]}")


def filter_by_priority(priority):
    """Фильтрует задачи по приоритету"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE priority = ?", (priority,))

    tasks = cursor.fetchall()
    conn.close()

    priority_names = {1: "низкий", 2: "средний", 3: "высокий"}
    print(
        f"\n📊 ЗАДАЧИ С ПРИОРИТЕТОМ: {priority_names.get(priority, priority)}")

    for task in tasks:
        print(f"[{task[0]}] {task[1]}")


def search_tasks(keyword):
    """Ищет задачи по ключевому слову"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # Ищем в названии и описании
    cursor.execute('''
    SELECT * from tasks 
    WHERE title LIKE ? OR description LIKE ?
    ''', (f"%{keyword}%", f"%{keyword}%"))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print(f"🔍 Задачи по запросу '{keyword}' не найдены")
        return

    print(f"\n🔍 РЕЗУЛЬТАТЫ ПОИСКА ('{keyword}'):")
    for task in tasks:
        print(f"[{task[0]}] {task[1]} - {task[4]}")


def filter_by_priority(priority):
    """Фильтрует задачи по приоритету"""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE priority = ?", (priority,))

    tasks = cursor.fetchall()
    conn.close()
    priority_names = {1: "низкий", 2: "средний", 3: "высокий"}
    print(
        f"\n📊 ЗАДАЧИ С ПРИОРИТЕТОМ: {priority_names.get(priority, "Неизвестно")}")

    for task in tasks:
        print(f"[{task[0]}] {task[1]}")


def show_menu():
    """Показывает меню"""
    print("\n" + "="*50)
    print("📋 УМНЫЙ СПИСОК ЗАДАЧ")
    print("="*50)
    print("1. Показать все задачи")
    print("2. Добавить задачу")
    print("3. Изменить статус задачи")
    print("4. Удалить задачу")
    print("5. Поиск задач")
    print("6. Фильтр по приоритету")
    print("7. Выход")
    print("="*50)


def main():
    """Главная функция с меню"""
    # Создаем таблицу при первом запуске
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority INTEGER DEFAULT 1,
        status TEXT DEFAULT 'todo',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

    while True:
        show_menu()
        choice = input("Выберите действие (1-7): ")

        if choice == "1":
            show_all_tasks()

        elif choice == "2":
            title = input("Название задачи: ")
            description = input("Описание (Enter чтобы пропустить): ")
            priority = input("Приоритет (1-низкий, 2-средний, 3-высокий): ")
            try:
                priority = int(priority) if priority else 1
                add_task(title, description, priority)
            except ValueError:
                print("❌ Приоритет должен быть числом 1-3")

        elif choice == "3":
            show_all_tasks()
            try:
                task_id = int(input("ID задачи для изменения: "))
                print("Статусы: todo, in_progress, done")
                new_status = input("Новый статус: ")
                update_task_status(task_id, new_status)
            except ValueError:
                print("❌ Введите корректный ID")

        elif choice == "4":
            show_all_tasks()
            try:
                task_id = int(input("ID задачи для удаления: "))
                delete_task(task_id)
            except ValueError:
                print("❌ Введите корректный ID")

        elif choice == "5":
            keyword = input("Введите слово для поиска: ")
            search_tasks(keyword)

        elif choice == "6":
            print("Приоритеты: 1-низкий, 2-средний, 3-высокий")
            try:
                priority = int(input("Введите приоритет: "))
                filter_by_priority(priority)
            except ValueError:
                print("❌ Введите число 1-3")

        elif choice == "7":
            print("👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter чтобы продолжить...")


# Тестируем
if __name__ == "__main__":
    main()
