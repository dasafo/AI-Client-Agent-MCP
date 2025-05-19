"""
Servicio para manejar la lógica de negocio relacionada con los clientes.
Incluye operaciones CRUD y otras operaciones específicas del dominio.
"""
from typing import Optional, Dict, Any
import logging
import asyncpg

# Configuración de logging
logger = logging.getLogger(__name__)

# Importaciones locales
from backend.models.client import ClientCreate, ClientUpdate

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

    async def get_client_by_id(self, client_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un cliente por su ID.
        
        Args:
            client_id: ID del cliente a buscar
            
        Returns:
            Dict con los datos del cliente o None si no se encuentra
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, name, email, phone, city, created_at, updated_at
                FROM clients
                WHERE id = $1
                """,
                client_id
            )
            return dict(row) if row else None

    async def get_client_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca un cliente por su dirección de correo electrónico.
        
        Args:
            email: Email del cliente a buscar
            
        Returns:
            Dict con los datos del cliente o None si no se encuentra
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, name, email, phone, city, created_at, updated_at
                FROM clients
                WHERE email = $1
                """,
                email.lower()
            )
            return dict(row) if row else None

    async def create_client(self, client: ClientCreate) -> Dict[str, Any]:
        """
        Crea un nuevo cliente en la base de datos.
        
        Args:
            client: Datos del cliente a crear
            
        Returns:
            Dict con los datos del cliente creado
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO clients (name, email, phone, city)
                VALUES ($1, $2, $3, $4)
                RETURNING id, name, email, phone, city, created_at, updated_at
                """,
                client.name,
                client.email.lower(),
                client.phone,
                client.city
            )
            return dict(row)
