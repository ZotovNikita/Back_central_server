import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.core.settings import settings
from src.api.base_router import base_router


tags = [
    {
      "name": "auth",
      "description": "Вход в админ-панель"
    },
    {
      "name": "users",
      "description": "Управление пользователями админ-панели"
    },
    {
      "name": "bots",
      "description": "Управление ботами"
    },
    {
      "name": "intents",
      "description": "Взаимодействие с интентами"
    },
    {
      "name": "client_chat",
      "description": "Взаимодействие с клиентским чатом"
    },
    {
      "name": "admin_chat",
      "description": "Взаимодействие с чатом в админ-панели"
    },
    {
      "name": "relations",
      "description": "Управление связями"
    },
    {
      "name": "ml",
      "description": "Взаимодействие с моделями"
    },
]

app = FastAPI(
    title='Центральный сервер',
    description="""
      Анекдот от ChatGPT:
      
      Однажды разработчики создали API, но они забыли задокументировать его.
      Они решили добавить Swagger для описания API и документации.
      Однако они были так увлечены написанием документации, что забыли реализовать сам API.
      Так что, когда кто-то попытался использовать их API, он вернул только один ответ: "Документация недоступна".
      
      Moral of the story: Не забывайте, что Swagger - это всего лишь инструмент для документирования вашего API, а не сам API.
    """,
    version='0.3.0',
    openapi_tags=tags,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
