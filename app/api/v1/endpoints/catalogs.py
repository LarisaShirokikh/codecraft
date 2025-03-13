from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# from app import crud, models, schemas
# from app.api import deps

router = APIRouter()

@router.get("/")
async def list_catalogs():
    """Получить список каталогов"""
    return {"message": "Список каталогов (заглушка)"}

