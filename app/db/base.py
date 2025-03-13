# base.py                 # Базовый класс моделей
# app/db/base.py
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

class CustomBase:
    # Генерирует имя таблицы автоматически из имени класса
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    # Общие поля для всех моделей
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base = declarative_base(cls=CustomBase)