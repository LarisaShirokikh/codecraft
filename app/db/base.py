# app/db/base.py
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, timezone

class CustomBase:
    # Автоматическое задание имени таблицы по имени класса
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Общие поля для всех моделей
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

# Явно аннотируем Base как DeclarativeMeta, чтобы Pylance понимал тип
Base: DeclarativeMeta = declarative_base(cls=CustomBase)