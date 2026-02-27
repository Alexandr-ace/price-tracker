from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Разрешаем запросы с любого источника (CORS) — для разработки
app.add_middleware(
    CORSMiddleware,
    # можно указать конкретные адреса, например ["http://localhost:5500"]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных, которую мы ожидаем от фронтенда


class Item(BaseModel):
    url: str

# Эндпоинт, который принимает POST-запросы по адресу /send-url


@app.post("/send-url")
async def send_url(item: Item):
    print(f"Получен URL: {item.url}")          # видим в консоли сервера
    return {
        "status": "Ха, получилось",
        "received_url": item.url,
        "message": f"Вы отправили URL: {item.url}"
    }

# Для проверки можно добавить корневой эндпоинт


@app.get("/")
async def root():
    return {"message": "Сервер работает!"}
