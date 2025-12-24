from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DATABASE_URL: str = "sqlite:///./todos.db"
    # postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME

    DATABASE_URL: str = 'postgresql+psycopg://postgres:00000@localhost:5432/Todo'

settings = Settings()
