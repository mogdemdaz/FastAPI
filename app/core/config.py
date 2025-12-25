import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DATABASE_URL: str = "sqlite:///./todos.db"
    # postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
    # DATABASE_URL: str = 'postgresql+psycopg://postgres:00000@localhost:5432/Todo'
    DATABASE_URL: str = 'postgresql://mogdemdaz:nhvRY685R1WKZs5wRxRrKS6iN2X8Aw9z@dpg-d56pva3uibrs739p2ms0-a/todo_nmal'
settings = Settings()


# class Settings(BaseSettings):
#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL",
#         "postgresql+psycopg://postgres:00000@localhost:5432/Todo"
#     )
#
# settings = Settings()