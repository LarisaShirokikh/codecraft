from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_users():
    """Получить список юзеров"""
    return {"message": "Список юзеров (заглушка)"}