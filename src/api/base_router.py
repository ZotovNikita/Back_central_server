from fastapi import APIRouter
from src.api import authorization


base_router = APIRouter()
base_router.include_router(authorization.router)
