from fastapi import APIRouter
from src.api import auth


base_router = APIRouter()
base_router.include_router(auth.router)
