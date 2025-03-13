from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_categories():
    """Получить список категорий"""
    return {"message": "Список категорий (заглушка)"}