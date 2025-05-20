from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Settings(BaseSettings):
    # Configuración de la base de datos
    DB_HOST: str = os.getenv("POSTGRES_SERVER", "localhost")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME: str = os.getenv("POSTGRES_DB", "test_db")
    DB_USER: str = os.getenv("POSTGRES_USER", "user")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")

    # Propiedad que retorna la URL de la base de datos
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Instancia de configuración global
settings = Settings()
