"""Модуль для настройки подключения к базе данных PostgreSQL."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Для локальной разработки через docker-compose
if not SQLALCHEMY_DATABASE_URL:
    DB_HOST = os.getenv("POSTGRES_HOST", "db")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "blog")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
