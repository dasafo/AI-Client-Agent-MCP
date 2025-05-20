"""
Servicio para manejar la lógica de negocio relacionada con los clientes.
Incluye operaciones CRUD y otras operaciones específicas del dominio.
"""

from typing import Optional, Dict, Any
import logging
import asyncpg

from backend.models.client import ClientCreate, ClientUpdate
from backend.repositories.client_repository import ClientRepository
from backend.repositories.client_note_repository import ClientNoteRepository
from backend.models.client_note import ClientNoteCreate

# Configuración de logging
logger = logging.getLogger(__name__)


class ClientService:
    """
    Servicio para gestionar las operaciones relacionadas con clientes.
    Se encarga de la lógica de negocio y la interacción con la base de datos.
    """

    def __init__(self, pool: asyncpg.Pool):
        """
        Inicializa el servicio con un pool de conexiones a la base de datos.

        Args:
            pool: Pool de conexiones a la base de datos
        """
        self.pool = pool
        self.repo = ClientRepository(pool)
        self.note_repo = ClientNoteRepository(pool)

    async def get_client_by_id(self, client_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un cliente por su ID.

        Args:
            client_id: ID del cliente a buscar

        Returns:
            Dict con los datos del cliente o None si no se encuentra
        """
        return await self.repo.get_by_id(client_id)

    async def get_client_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca un cliente por su dirección de correo electrónico.

        Args:
            email: Email del cliente a buscar

        Returns:
            Dict con los datos del cliente o None si no se encuentra
        """

        return await self.repo.get_by_email(email)

    async def create_client(self, client: ClientCreate) -> Dict[str, Any]:
        """
        Crea un nuevo cliente en la base de datos.

        Args:
            client: Datos del cliente a crear

        Returns:
            Dict con los datos del cliente creado
        """
        return await self.repo.create(client)

    async def update_client(
        self, client_id: int, update_data: ClientUpdate
    ) -> Optional[Dict[str, Any]]:
        """
        Actualiza un cliente existente por su ID.

        Args:
            client_id: ID del cliente a actualizar
            update_data: Datos a actualizar (pueden ser parciales)

        Returns:
            Dict con los datos actualizados o None si no se encuentra
        """
        return await self.repo.update(client_id, update_data)

    async def delete_client(self, client_id: int) -> bool:
        """
        Elimina un cliente por su ID.

        Args:
            client_id: ID del cliente a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        return await self.repo.delete(client_id)

    async def list_clients(
        self,
        name: Optional[str] = None,
        city: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Dict[str, Any]]:
        """
        Lista los clientes en la base de datos con opciones de filtrado y paginación.

        Args:
            name: Nombre del cliente a buscar (opcional)
            city: Ciudad del cliente a buscar (opcional)
            limit: Número máximo de clientes a retornar
            offset: Desplazamiento para la paginación

        Returns:
            Lista de diccionarios con los datos de los clientes
        """
        return await self.repo.list_clients(
            name=name, city=city, limit=limit, offset=offset
        )

    async def add_note(self, note: ClientNoteCreate) -> Dict[str, Any]:
        """
        Añade una nota a un cliente.

        Args:
            note: Datos de la nota a añadir

        Returns:
            Dict con los datos de la nota añadida
        """
        return await self.note_repo.add_note(note)

    async def list_notes(self, client_id: int) -> list[Dict[str, Any]]:
        """
        Lista las notas de un cliente.

        Args:
            client_id: ID del cliente cuyas notas se quieren listar

        Returns:
            Lista de diccionarios con los datos de las notas del cliente
        """
        return await self.note_repo.list_notes(client_id)
