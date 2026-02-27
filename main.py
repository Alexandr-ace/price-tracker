from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Создаем приложение
app = FastAPI()

# Первый endpoint (маршрут)


@app.get("/")
def read_root():
    return {"message": "Привет, это мой первый FastAPI!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Привет, {name}!"}


@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}


app = FastAPI()

# Модель данных (схема)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# Данные в памяти (вместо БД)
fake_db = []


@app.post("/items/")
def create_item(item: Item):
    """Создание нового товара"""
    fake_db.append(item)
    return {"message": "Товар создан", "item": item}


@app.get("/items/")
def get_items():
    """Получение всех товаров"""
    return {"items": fake_db}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Получение товара по ID"""
    if 0 <= item_id < len(fake_db):
        return fake_db[item_id]
    return {"error": "Товар не найден"}
