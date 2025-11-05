

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Добавляем корневую директорию в Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Загружаем переменные окружения
load_dotenv()

# Импортируем ваши модели
from module_4.app.models.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

def get_url():
    user = os.getenv('POSTGRES_USER', 'techcore')
    password = os.getenv('POSTGRES_PASSWORD', 'techcore')
    server = os.getenv('POSTGRES_SERVER', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')  # значение по умолчанию
    db = os.getenv('POSTGRES_DB', 'techcore')
    return f"postgresql://{user}:{password}@{server}:{port}/{db}"

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()