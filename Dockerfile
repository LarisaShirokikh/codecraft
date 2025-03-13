FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

# Настройка poetry для отключения создания виртуального окружения
RUN poetry config virtualenvs.create false

# Установка зависимостей
RUN poetry install --no-root --without dev

COPY . .

RUN poetry install --without dev
EXPOSE 8000
CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000"]