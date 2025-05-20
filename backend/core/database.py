import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from .config import settings


class Database:
    """
    Clase para gestionar la conexión a la base de datos PostgreSQL de forma asíncrona.
    Utiliza un pool de conexiones para mejorar el rendimiento.
    """

    def __init__(self):
        # Inicializa el pool de conexiones como None
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """
        Establece la conexión con la base de datos si no existe un pool activo.
        Crea un pool de conexiones con los parámetros definidos en la configuración.

        Returns:
            asyncpg.Pool: Pool de conexiones a la base de datos
        """
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                dsn=settings.DATABASE_URL,  # URL de conexión a la base de datos
                min_size=1,  # Tamaño mínimo del pool
                max_size=10,  # Tamaño máximo del pool
                command_timeout=60,  # Tiempo máximo de espera por comando (segundos)
            )
        return self._pool

    async def disconnect(self):
        """
        Cierra todas las conexiones del pool y lo establece a None.
        Debe llamarse al finalizar la aplicación para liberar recursos.
        """
        if self._pool:
            await self._pool.close()  # Cierra todas las conexiones del pool
            self._pool = None  # Elimina la referencia al pool

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[asyncpg.Connection]:
        """
        Context manager para manejar conexiones a la base de datos de forma segura.

        Yields:
            asyncpg.Connection: Conexión a la base de datos

        Raises:
            Exception: Cualquier error ocurrido durante la transacción
        """
        # Asegura que exista un pool de conexiones
        if not self._pool:
            await self.connect()
        if self._pool is None:
            raise RuntimeError("Database connection pool is not initialized.")

        # Obtiene una conexión del pool
        async with self._pool.acquire() as connection:
            try:
                # Entrega la conexión al bloque with
                yield connection
            except Exception as e:
                # No se puede hacer rollback fuera de una transacción explícita
                raise e
            # No se hace commit aquí, asyncpg maneja autocommit fuera de transacciones

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[asyncpg.Connection]:
        """
        Context manager para manejar transacciones en la base de datos.
        Asegura que la transacción se realice correctamente o se revierta en caso de error.
        Yields:
            asyncpg.Connection: Conexión a la base de datos dentro de una transacción
        Raises:
            Exception: Cualquier error ocurrido durante la transacción
        """
        if not self._pool:
            await self.connect()
        if self._pool is None:
            raise RuntimeError("Database connection pool is not initialized.")

        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    yield connection
                except Exception as e:
                    await connection.rollback()
                    raise e


# Instancia global de la base de datos
database = Database()
