from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импорт моделей и метаданных
from app.models import Base  # Убедись, что путь правильный

config = context.config

# Настройка логирования, если есть файл конфигурации
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Передаём метаданные Alembic
target_metadata = Base.metadata

def run_migrations_offline():
    """Миграции в offline-режиме (без подключения к БД)"""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Миграции в online-режиме (с подключением к БД)"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()  
    # 6