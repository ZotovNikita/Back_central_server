from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
      "name": "client_chat",
      "description": "Взаимодействие с клиентским чатом"
    },
    {
      "name": "intents",
      "description": "Взаимодействие с интентами"
    },
]

app = FastAPI(
    title='Центральный сервер',
    description='Здесь бамбук не курят.',
    version='0.1.2',
    openapi_tags=tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
