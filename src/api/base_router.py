from fastapi import APIRouter
from src.api import auth, users, bots, chat, intents


base_router = APIRouter()
base_router.include_router(auth.router)
base_router.include_router(users.router)
base_router.include_router(bots.router)
base_router.include_router(chat.router)
base_router.include_router(intents.router)
