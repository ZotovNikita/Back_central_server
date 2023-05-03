from fastapi import APIRouter
from src.api import auth, users, bots, intents, client_chat, admin_chat, relations, ml


base_router = APIRouter()
base_router.include_router(auth.router)
base_router.include_router(users.router)
base_router.include_router(bots.router)
base_router.include_router(intents.router)
base_router.include_router(client_chat.router)
base_router.include_router(admin_chat.router)
base_router.include_router(relations.router)
base_router.include_router(ml.router)


@base_router.get('/', name='Default page')
async def default():
    return 'You are great!'
