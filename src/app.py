from fastapi import FastAPI
from src.api.base_router import base_router


tags = [
    ...
]

app = FastAPI(
    title='Центральный сервер',
    description='Здесь бамбук не курят.',
    version='0.0.1',
    openapi_tags=tags,
)

app.include_router(base_router)
