from fastapi import APIRouter, Depends
from src.services.auth import get_current_user


router = APIRouter(
    prefix='/intents',
    tags=['intents'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/get', name='Тест получения интентов')
def get():
    data = {f'Intent {i}': f'Что-то {i}' for i in range(30)}
    return data
