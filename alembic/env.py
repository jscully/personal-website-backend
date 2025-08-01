from logging.config import fileConfig
from sqlalchemy import engine_from_config  # type: ignore
from sqlalchemy import pool  # type: ignore
from alembic import context
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.base import Base
from app.models.blog import Blog
from app.models.tag import Tag
from app.models.contact import Contact
from app.models.user import User

config = context.config

if config.config_file_name is not None and os.path.exists(config.config_file_name):
    try:
        fileConfig(config.config_file_name)
    except Exception:
        pass

database_url = os.environ.get("DATABASE_URL")

if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
else:
    config.set_main_option(
        "sqlalchemy.url",
        "postgresql://postgres:postgres@localhost:5432/personal_website",
    )

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
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
