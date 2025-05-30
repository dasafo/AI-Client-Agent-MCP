# backend/core/database.py
import asyncpg
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la URL de conexión a la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    """
    Clase para gestionar la conexión a la base de datos PostgreSQL.
    Implementa un patrón singleton para el pool de conexiones.
    """
    def __init__(self):
        # Inicializa el pool de conexiones como None
        self._pool = None

    async def connect(self):
        """
        Establece la conexión con la base de datos si no existe.
        Crea un pool de conexiones para reutilizarlas eficientemente.
        
        Returns:
            Pool de conexiones a la base de datos.
        """
        if not self._pool:
            # Crea un nuevo pool de conexiones si no existe
            self._pool = await asyncpg.create_pool(
                dsn=DATABASE_URL, min_size=1, max_size=10
            )
        return self._pool

    async def disconnect(self):
        """
        Cierra el pool de conexiones a la base de datos si está activo.
        """
        if self._pool:
            # Cierra todas las conexiones en el pool
            await self._pool.close()
            self._pool = None


# Instancia única de la clase Database para ser utilizada en toda la aplicación
database = Database()
